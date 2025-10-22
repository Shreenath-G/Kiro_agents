import json
import os
import boto3
from datetime import datetime, timedelta
from decimal import Decimal
from boto3.dynamodb.conditions import Key

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = os.environ.get('BUCKET_NAME')
METRICS_TABLE = os.environ.get('METRICS_TABLE')

def handler(event, context):
    """
    Budget optimization tool for the AI agent.
    Optimizes budget allocation across campaigns and platforms.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Handle warming requests (prevents cold starts)
    if event.get('source') == 'warming':
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'warm', 'timestamp': datetime.now().isoformat()})
        }
    
    api_path = event.get('apiPath', '')
    http_method = event.get('httpMethod', '')
    parameters = event.get('parameters', [])
    request_body = event.get('requestBody', {})
    
    # Handle health checks
    if api_path == '/health':
        return success_response(event, {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'function': 'budget-optimizer'
        })
    
    # Handle POST OPTIMIZE BUDGET
    if http_method == 'POST' and '/optimize' in api_path:
        body_data = parse_request_body(request_body)
        total_budget = body_data.get('totalBudget')
        campaign_ids = body_data.get('campaignIds', [])
        optimization_goal = body_data.get('goal', 'maximize_roas')  # maximize_roas, minimize_cpa, maximize_conversions
        
        if not total_budget or not campaign_ids:
            return error_response(event, 'totalBudget and campaignIds required')
        
        allocation = optimize_budget_allocation(total_budget, campaign_ids, optimization_goal)
        return success_response(event, allocation)
    
    # Handle POST REALLOCATE
    elif http_method == 'POST' and '/reallocate' in api_path:
        body_data = parse_request_body(request_body)
        from_campaign = body_data.get('fromCampaign')
        to_campaign = body_data.get('toCampaign')
        amount = body_data.get('amount')
        
        if not from_campaign or not to_campaign or not amount:
            return error_response(event, 'fromCampaign, toCampaign, and amount required')
        
        result = reallocate_budget(from_campaign, to_campaign, amount)
        return success_response(event, result)
    
    # Handle GET BUDGET RECOMMENDATIONS
    elif http_method == 'GET' and '/recommendations' in api_path:
        total_budget = float(get_parameter(parameters, 'totalBudget') or 0)
        
        if not total_budget:
            return error_response(event, 'totalBudget parameter required')
        
        recommendations = get_budget_recommendations(total_budget)
        return success_response(event, recommendations)
    
    # Handle POST SIMULATE
    elif http_method == 'POST' and '/simulate' in api_path:
        body_data = parse_request_body(request_body)
        budget_scenarios = body_data.get('scenarios', [])
        
        if not budget_scenarios:
            return error_response(event, 'scenarios required')
        
        simulation = simulate_budget_scenarios(budget_scenarios)
        return success_response(event, simulation)
    
    else:
        return error_response(event, 'Invalid operation')

def optimize_budget_allocation(total_budget, campaign_ids, optimization_goal='maximize_roas'):
    """
    Optimize budget allocation across campaigns based on performance.
    Uses a simple weighted allocation based on historical performance.
    """
    # Get performance data for all campaigns
    campaign_performance = []
    
    for campaign_id in campaign_ids:
        metrics = get_campaign_metrics(campaign_id)
        if metrics:
            campaign_performance.append({
                'campaignId': campaign_id,
                'roas': metrics.get('roas', 0),
                'cpa': metrics.get('cpa', 999),
                'conversions': metrics.get('conversions', 0),
                'currentBudget': metrics.get('budget', 0)
            })
    
    if not campaign_performance:
        return {
            'status': 'error',
            'message': 'No performance data available for campaigns'
        }
    
    # Calculate allocation based on optimization goal
    if optimization_goal == 'maximize_roas':
        # Allocate more to campaigns with higher ROAS
        total_roas = sum(c['roas'] for c in campaign_performance)
        if total_roas == 0:
            # Equal allocation if no ROAS data
            allocation_weights = [1/len(campaign_performance)] * len(campaign_performance)
        else:
            allocation_weights = [c['roas'] / total_roas for c in campaign_performance]
    
    elif optimization_goal == 'minimize_cpa':
        # Allocate more to campaigns with lower CPA (inverse weighting)
        inverse_cpas = [1/c['cpa'] if c['cpa'] > 0 else 0 for c in campaign_performance]
        total_inverse_cpa = sum(inverse_cpas)
        if total_inverse_cpa == 0:
            allocation_weights = [1/len(campaign_performance)] * len(campaign_performance)
        else:
            allocation_weights = [inv_cpa / total_inverse_cpa for inv_cpa in inverse_cpas]
    
    elif optimization_goal == 'maximize_conversions':
        # Allocate based on conversion volume
        total_conversions = sum(c['conversions'] for c in campaign_performance)
        if total_conversions == 0:
            allocation_weights = [1/len(campaign_performance)] * len(campaign_performance)
        else:
            allocation_weights = [c['conversions'] / total_conversions for c in campaign_performance]
    
    else:
        # Default to equal allocation
        allocation_weights = [1/len(campaign_performance)] * len(campaign_performance)
    
    # Apply minimum budget constraints (at least 10% to each campaign)
    min_allocation = 0.10
    adjusted_weights = []
    remaining_budget_pct = 1.0 - (min_allocation * len(campaign_performance))
    
    for weight in allocation_weights:
        adjusted_weight = min_allocation + (weight * remaining_budget_pct)
        adjusted_weights.append(adjusted_weight)
    
    # Calculate actual budget allocations
    allocations = []
    for i, campaign in enumerate(campaign_performance):
        allocated_budget = round(total_budget * adjusted_weights[i], 2)
        change_from_current = allocated_budget - campaign['currentBudget']
        change_pct = (change_from_current / campaign['currentBudget'] * 100) if campaign['currentBudget'] > 0 else 0
        
        allocations.append({
            'campaignId': campaign['campaignId'],
            'currentBudget': campaign['currentBudget'],
            'recommendedBudget': allocated_budget,
            'change': round(change_from_current, 2),
            'changePct': round(change_pct, 1),
            'weight': round(adjusted_weights[i] * 100, 1),
            'roas': campaign['roas'],
            'cpa': campaign['cpa']
        })
    
    # Calculate expected outcomes
    expected_total_conversions = sum(
        (alloc['recommendedBudget'] / campaign_performance[i]['cpa']) 
        for i, alloc in enumerate(allocations) 
        if campaign_performance[i]['cpa'] > 0
    )
    
    expected_avg_roas = sum(
        (alloc['weight'] / 100 * campaign_performance[i]['roas']) 
        for i, alloc in enumerate(allocations)
    )
    
    return {
        'optimizationGoal': optimization_goal,
        'totalBudget': total_budget,
        'allocations': allocations,
        'expectedOutcomes': {
            'totalConversions': round(expected_total_conversions, 0),
            'avgROAS': round(expected_avg_roas, 2),
            'estimatedRevenue': round(expected_total_conversions * 50, 2)  # Assuming $50 AOV
        },
        'summary': {
            'campaignsOptimized': len(allocations),
            'budgetIncreases': len([a for a in allocations if a['change'] > 0]),
            'budgetDecreases': len([a for a in allocations if a['change'] < 0])
        },
        'timestamp': datetime.now().isoformat()
    }

def reallocate_budget(from_campaign, to_campaign, amount):
    """Reallocate budget from one campaign to another."""
    return {
        'fromCampaign': from_campaign,
        'toCampaign': to_campaign,
        'amount': amount,
        'status': 'success',
        'message': f'Reallocated ${amount} from {from_campaign} to {to_campaign}',
        'timestamp': datetime.now().isoformat()
    }

def get_budget_recommendations(total_budget):
    """Get budget allocation recommendations across all campaigns."""
    # Get all campaigns
    all_campaigns = [
        'goog-camp-001', 'goog-camp-002', 'goog-camp-003',
        'meta-camp-001', 'meta-camp-002', 'meta-camp-003'
    ]
    
    # Optimize for maximum ROAS
    optimization = optimize_budget_allocation(total_budget, all_campaigns, 'maximize_roas')
    
    # Add platform-level recommendations
    google_budget = sum(a['recommendedBudget'] for a in optimization['allocations'] if 'goog' in a['campaignId'])
    meta_budget = sum(a['recommendedBudget'] for a in optimization['allocations'] if 'meta' in a['campaignId'])
    
    recommendations = {
        'totalBudget': total_budget,
        'platformAllocation': {
            'google': {
                'budget': round(google_budget, 2),
                'percentage': round(google_budget / total_budget * 100, 1)
            },
            'meta': {
                'budget': round(meta_budget, 2),
                'percentage': round(meta_budget / total_budget * 100, 1)
            }
        },
        'campaignAllocations': optimization['allocations'],
        'expectedOutcomes': optimization['expectedOutcomes'],
        'keyRecommendations': [
            'Focus budget on high-ROAS campaigns',
            'Maintain minimum spend on testing campaigns',
            'Review and adjust weekly based on performance'
        ],
        'timestamp': datetime.now().isoformat()
    }
    
    return recommendations

def simulate_budget_scenarios(scenarios):
    """Simulate different budget allocation scenarios."""
    results = []
    
    for scenario in scenarios:
        scenario_name = scenario.get('name', 'Unnamed')
        total_budget = scenario.get('totalBudget', 0)
        allocations = scenario.get('allocations', {})
        
        # Calculate expected outcomes for this scenario
        expected_conversions = 0
        expected_cost = 0
        
        for campaign_id, budget in allocations.items():
            metrics = get_campaign_metrics(campaign_id)
            if metrics and metrics.get('cpa', 0) > 0:
                conversions = budget / metrics['cpa']
                expected_conversions += conversions
                expected_cost += budget
        
        expected_roas = (expected_conversions * 50) / expected_cost if expected_cost > 0 else 0
        
        results.append({
            'scenario': scenario_name,
            'totalBudget': total_budget,
            'expectedConversions': round(expected_conversions, 0),
            'expectedROAS': round(expected_roas, 2),
            'expectedRevenue': round(expected_conversions * 50, 2)
        })
    
    # Identify best scenario
    best_scenario = max(results, key=lambda x: x['expectedROAS']) if results else None
    
    return {
        'scenarios': results,
        'bestScenario': best_scenario['scenario'] if best_scenario else None,
        'recommendation': f"Scenario '{best_scenario['scenario']}' provides the best ROAS" if best_scenario else "No clear winner",
        'timestamp': datetime.now().isoformat()
    }

def get_campaign_metrics(campaign_id):
    """Get latest metrics for a campaign from DynamoDB."""
    try:
        table = dynamodb.Table(METRICS_TABLE)
        
        # Query for the most recent metrics
        response = table.query(
            KeyConditionExpression=Key('campaignId').eq(campaign_id),
            ScanIndexForward=False,  # Descending order
            Limit=1
        )
        
        items = response.get('Items', [])
        if items:
            item = items[0]
            return {
                'campaignId': campaign_id,
                'roas': float(item.get('roas', 0)) if 'roas' in item else 0,
                'cpa': float(item.get('cpa', 0)) if 'cpa' in item else 0,
                'conversions': float(item.get('conversions', 0)) if 'conversions' in item else 0,
                'cost': float(item.get('cost', 0)) if 'cost' in item else 0,
                'budget': 1000  # Default budget, should be fetched from campaign data
            }
        
        return None
        
    except Exception as e:
        print(f"Error getting metrics: {str(e)}")
        return None

def get_parameter(parameters, name):
    """Extract parameter value by name."""
    for param in parameters:
        if param.get('name') == name:
            return param.get('value')
    return None

def parse_request_body(request_body):
    """Parse request body from Bedrock Agent format."""
    if not request_body:
        return {}
    content = request_body.get('content', {})
    body_str = content.get('application/json', '')
    if body_str:
        try:
            return json.loads(body_str)
        except json.JSONDecodeError:
            return {}
    return {}

def success_response(event, data):
    return {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': event.get('actionGroup'),
            'apiPath': event.get('apiPath'),
            'httpMethod': event.get('httpMethod'),
            'httpStatusCode': 200,
            'responseBody': {
                'application/json': {
                    'body': json.dumps(data, default=str)
                }
            }
        }
    }

def error_response(event, error_message):
    return {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': event.get('actionGroup'),
            'apiPath': event.get('apiPath'),
            'httpMethod': event.get('httpMethod'),
            'httpStatusCode': 400,
            'responseBody': {
                'application/json': {
                    'body': json.dumps({'error': error_message})
                }
            }
        }
    }
