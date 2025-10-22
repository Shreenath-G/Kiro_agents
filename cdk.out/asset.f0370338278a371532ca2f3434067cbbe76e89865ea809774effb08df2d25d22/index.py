import json
import os
import boto3
from datetime import datetime, timedelta
from decimal import Decimal

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
secrets_client = boto3.client('secretsmanager')

BUCKET_NAME = os.environ.get('BUCKET_NAME')
METRICS_TABLE = os.environ.get('METRICS_TABLE')
SECRETS_ARN = os.environ.get('SECRETS_ARN')

def handler(event, context):
    """
    Google Ads integration tool for the AI agent.
    Manages Google Ads campaigns: get metrics, adjust bids, update budgets.
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
            'function': 'google-ads'
        })
    
    # Get API credentials (in production, use real Google Ads API)
    # For demo, we'll simulate the API calls
    
    # Handle GET CAMPAIGNS
    if http_method == 'GET' and '/campaigns' in api_path:
        campaigns = get_campaigns()
        return success_response(event, {'campaigns': campaigns})
    
    # Handle GET METRICS
    elif http_method == 'GET' and '/metrics' in api_path:
        campaign_id = get_parameter(parameters, 'campaignId')
        if not campaign_id:
            return error_response(event, 'campaignId parameter required')
        
        metrics = get_campaign_metrics(campaign_id)
        return success_response(event, metrics)
    
    # Handle POST ADJUST BID
    elif http_method == 'POST' and '/adjust-bid' in api_path:
        body_data = parse_request_body(request_body)
        campaign_id = body_data.get('campaignId')
        bid_adjustment = body_data.get('bidAdjustment')  # percentage
        
        if not campaign_id or bid_adjustment is None:
            return error_response(event, 'campaignId and bidAdjustment required')
        
        result = adjust_campaign_bid(campaign_id, bid_adjustment)
        return success_response(event, result)
    
    # Handle POST UPDATE BUDGET
    elif http_method == 'POST' and '/update-budget' in api_path:
        body_data = parse_request_body(request_body)
        campaign_id = body_data.get('campaignId')
        new_budget = body_data.get('newBudget')
        
        if not campaign_id or not new_budget:
            return error_response(event, 'campaignId and newBudget required')
        
        result = update_campaign_budget(campaign_id, new_budget)
        return success_response(event, result)
    
    # Handle POST PAUSE/ACTIVATE
    elif http_method == 'POST' and '/toggle-status' in api_path:
        body_data = parse_request_body(request_body)
        campaign_id = body_data.get('campaignId')
        status = body_data.get('status')  # 'PAUSED' or 'ENABLED'
        
        if not campaign_id or not status:
            return error_response(event, 'campaignId and status required')
        
        result = toggle_campaign_status(campaign_id, status)
        return success_response(event, result)
    
    else:
        return error_response(event, 'Invalid operation')

def get_campaigns():
    """Get list of Google Ads campaigns (simulated)."""
    # In production, use Google Ads API
    return [
        {
            'id': 'goog-camp-001',
            'name': 'Search - Brand Keywords',
            'status': 'ENABLED',
            'budget': 1500,
            'platform': 'google'
        },
        {
            'id': 'goog-camp-002',
            'name': 'Display - Remarketing',
            'status': 'ENABLED',
            'budget': 800,
            'platform': 'google'
        },
        {
            'id': 'goog-camp-003',
            'name': 'Shopping - Product Ads',
            'status': 'ENABLED',
            'budget': 2000,
            'platform': 'google'
        }
    ]

def get_campaign_metrics(campaign_id):
    """Get campaign performance metrics (simulated)."""
    # In production, fetch from Google Ads API
    # For demo, generate realistic metrics
    import random
    
    base_metrics = {
        'goog-camp-001': {'impressions': 45000, 'clicks': 2250, 'conversions': 180, 'cost': 1450},
        'goog-camp-002': {'impressions': 120000, 'clicks': 960, 'conversions': 48, 'cost': 780},
        'goog-camp-003': {'impressions': 35000, 'clicks': 1750, 'conversions': 210, 'cost': 1980},
    }
    
    metrics = base_metrics.get(campaign_id, {
        'impressions': random.randint(10000, 50000),
        'clicks': random.randint(500, 2500),
        'conversions': random.randint(20, 200),
        'cost': random.randint(500, 2000)
    })
    
    # Calculate derived metrics
    metrics['ctr'] = round((metrics['clicks'] / metrics['impressions']) * 100, 2) if metrics['impressions'] > 0 else 0
    metrics['cpc'] = round(metrics['cost'] / metrics['clicks'], 2) if metrics['clicks'] > 0 else 0
    metrics['conversion_rate'] = round((metrics['conversions'] / metrics['clicks']) * 100, 2) if metrics['clicks'] > 0 else 0
    metrics['cpa'] = round(metrics['cost'] / metrics['conversions'], 2) if metrics['conversions'] > 0 else 0
    metrics['campaignId'] = campaign_id
    metrics['timestamp'] = datetime.now().isoformat()
    
    # Store in DynamoDB
    store_metrics(campaign_id, metrics)
    
    return metrics

def adjust_campaign_bid(campaign_id, bid_adjustment):
    """Adjust campaign bid by percentage."""
    # In production, use Google Ads API
    return {
        'campaignId': campaign_id,
        'bidAdjustment': bid_adjustment,
        'status': 'success',
        'message': f'Bid adjusted by {bid_adjustment}% for campaign {campaign_id}',
        'timestamp': datetime.now().isoformat()
    }

def update_campaign_budget(campaign_id, new_budget):
    """Update campaign daily budget."""
    # In production, use Google Ads API
    return {
        'campaignId': campaign_id,
        'newBudget': new_budget,
        'status': 'success',
        'message': f'Budget updated to ${new_budget} for campaign {campaign_id}',
        'timestamp': datetime.now().isoformat()
    }

def toggle_campaign_status(campaign_id, status):
    """Pause or activate campaign."""
    # In production, use Google Ads API
    return {
        'campaignId': campaign_id,
        'status': status,
        'message': f'Campaign {campaign_id} status changed to {status}',
        'timestamp': datetime.now().isoformat()
    }

def store_metrics(campaign_id, metrics):
    """Store metrics in DynamoDB."""
    try:
        table = dynamodb.Table(METRICS_TABLE)
        item = {
            'campaignId': campaign_id,
            'timestamp': int(datetime.now().timestamp()),
            'ttl': int((datetime.now() + timedelta(days=90)).timestamp()),
            **{k: Decimal(str(v)) if isinstance(v, (int, float)) else v 
               for k, v in metrics.items() if k not in ['campaignId', 'timestamp']}
        }
        table.put_item(Item=item)
    except Exception as e:
        print(f"Error storing metrics: {str(e)}")

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
