import json
import os
import boto3
from datetime import datetime, timedelta
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import statistics

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = os.environ.get('BUCKET_NAME')
METRICS_TABLE = os.environ.get('METRICS_TABLE')

def handler(event, context):
    """
    Performance analytics tool for the AI agent.
    Analyzes campaign performance, identifies trends, and predicts outcomes.
    """
    print(f"Received event: {json.dumps(event)}")
    
    api_path = event.get('apiPath', '')
    http_method = event.get('httpMethod', '')
    parameters = event.get('parameters', [])
    request_body = event.get('requestBody', {})
    
    # Handle GET PERFORMANCE ANALYSIS
    if http_method == 'GET' and '/analyze-performance' in api_path:
        campaign_id = get_parameter(parameters, 'campaignId')
        days = int(get_parameter(parameters, 'days') or 7)
        
        if not campaign_id:
            return error_response(event, 'campaignId parameter required')
        
        analysis = analyze_campaign_performance(campaign_id, days)
        return success_response(event, analysis)
    
    # Handle GET TREND DETECTION
    elif http_method == 'GET' and '/detect-trends' in api_path:
        campaign_id = get_parameter(parameters, 'campaignId')
        
        if not campaign_id:
            return error_response(event, 'campaignId parameter required')
        
        trends = detect_performance_trends(campaign_id)
        return success_response(event, trends)
    
    # Handle POST COMPARE CAMPAIGNS
    elif http_method == 'POST' and '/compare-campaigns' in api_path:
        body_data = parse_request_body(request_body)
        campaign_ids = body_data.get('campaignIds', [])
        
        if not campaign_ids or len(campaign_ids) < 2:
            return error_response(event, 'At least 2 campaignIds required')
        
        comparison = compare_campaigns(campaign_ids)
        return success_response(event, comparison)
    
    # Handle GET RECOMMENDATIONS
    elif http_method == 'GET' and '/recommendations' in api_path:
        campaign_id = get_parameter(parameters, 'campaignId')
        
        if not campaign_id:
            return error_response(event, 'campaignId parameter required')
        
        recommendations = generate_recommendations(campaign_id)
        return success_response(event, recommendations)
    
    # Handle GET CROSS-PLATFORM ANALYSIS
    elif http_method == 'GET' and '/cross-platform' in api_path:
        analysis = analyze_cross_platform_performance()
        return success_response(event, analysis)
    
    else:
        return error_response(event, 'Invalid operation')

def analyze_campaign_performance(campaign_id, days=7):
    """Analyze campaign performance over time period."""
    try:
        table = dynamodb.Table(METRICS_TABLE)
        
        # Query metrics for the campaign
        start_time = int((datetime.now() - timedelta(days=days)).timestamp())
        response = table.query(
            KeyConditionExpression=Key('campaignId').eq(campaign_id) & Key('timestamp').gte(start_time)
        )
        
        items = response.get('Items', [])
        
        if not items:
            return {
                'campaignId': campaign_id,
                'status': 'insufficient_data',
                'message': 'Not enough data for analysis'
            }
        
        # Calculate aggregate metrics
        total_impressions = sum(float(item.get('impressions', 0)) for item in items)
        total_clicks = sum(float(item.get('clicks', 0)) for item in items)
        total_conversions = sum(float(item.get('conversions', 0)) for item in items)
        total_cost = sum(float(item.get('cost', 0)) for item in items)
        
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
        avg_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        avg_cpa = (total_cost / total_conversions) if total_conversions > 0 else 0
        
        # Calculate trends
        recent_items = items[-3:] if len(items) >= 3 else items
        older_items = items[:3] if len(items) >= 6 else items[:len(items)//2]
        
        recent_ctr = statistics.mean([float(item.get('ctr', 0)) for item in recent_items])
        older_ctr = statistics.mean([float(item.get('ctr', 0)) for item in older_items])
        ctr_trend = 'improving' if recent_ctr > older_ctr else 'declining' if recent_ctr < older_ctr else 'stable'
        
        recent_cpa = statistics.mean([float(item.get('cpa', 0)) for item in recent_items if float(item.get('cpa', 0)) > 0])
        older_cpa = statistics.mean([float(item.get('cpa', 0)) for item in older_items if float(item.get('cpa', 0)) > 0])
        cpa_trend = 'improving' if recent_cpa < older_cpa else 'declining' if recent_cpa > older_cpa else 'stable'
        
        # Detect issues
        issues = []
        if avg_ctr < 1.0:
            issues.append('Low CTR - consider improving ad copy or targeting')
        if avg_conversion_rate < 2.0:
            issues.append('Low conversion rate - review landing page and offer')
        if ctr_trend == 'declining':
            issues.append('CTR declining - possible ad fatigue')
        if cpa_trend == 'declining':
            issues.append('CPA increasing - efficiency dropping')
        
        return {
            'campaignId': campaign_id,
            'period': f'{days} days',
            'dataPoints': len(items),
            'aggregateMetrics': {
                'totalImpressions': int(total_impressions),
                'totalClicks': int(total_clicks),
                'totalConversions': int(total_conversions),
                'totalCost': round(total_cost, 2),
                'avgCTR': round(avg_ctr, 2),
                'avgCPC': round(avg_cpc, 2),
                'avgConversionRate': round(avg_conversion_rate, 2),
                'avgCPA': round(avg_cpa, 2),
                'roas': round((total_conversions * 50) / total_cost, 2) if total_cost > 0 else 0  # Assuming $50 avg order value
            },
            'trends': {
                'ctr': ctr_trend,
                'cpa': cpa_trend
            },
            'issues': issues,
            'overallHealth': 'good' if len(issues) == 0 else 'needs_attention' if len(issues) <= 2 else 'critical',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error analyzing performance: {str(e)}")
        return {
            'campaignId': campaign_id,
            'status': 'error',
            'message': str(e)
        }

def detect_performance_trends(campaign_id):
    """Detect specific performance trends and anomalies."""
    analysis = analyze_campaign_performance(campaign_id, days=14)
    
    trends = {
        'campaignId': campaign_id,
        'detectedTrends': [],
        'anomalies': [],
        'predictions': {}
    }
    
    # Analyze trends from the performance data
    if analysis.get('trends', {}).get('ctr') == 'declining':
        trends['detectedTrends'].append({
            'type': 'ad_fatigue',
            'severity': 'medium',
            'description': 'CTR declining over time, indicating possible ad fatigue',
            'recommendation': 'Refresh ad creatives or test new variations'
        })
    
    if analysis.get('trends', {}).get('cpa') == 'declining':
        trends['detectedTrends'].append({
            'type': 'efficiency_drop',
            'severity': 'high',
            'description': 'Cost per acquisition increasing',
            'recommendation': 'Review targeting, optimize bids, or improve landing page'
        })
    
    # Check for anomalies
    metrics = analysis.get('aggregateMetrics', {})
    if metrics.get('avgCTR', 0) < 0.5:
        trends['anomalies'].append({
            'type': 'low_ctr',
            'value': metrics.get('avgCTR'),
            'threshold': 1.0,
            'action': 'urgent_review_needed'
        })
    
    # Make predictions
    current_roas = metrics.get('roas', 0)
    if current_roas > 0:
        trends['predictions']['nextWeekROAS'] = round(current_roas * 0.95, 2)  # Conservative estimate
        trends['predictions']['confidence'] = 'medium'
    
    return trends

def compare_campaigns(campaign_ids):
    """Compare performance across multiple campaigns."""
    comparisons = []
    
    for campaign_id in campaign_ids:
        analysis = analyze_campaign_performance(campaign_id, days=7)
        comparisons.append({
            'campaignId': campaign_id,
            'metrics': analysis.get('aggregateMetrics', {}),
            'health': analysis.get('overallHealth', 'unknown')
        })
    
    # Identify best and worst performers
    comparisons_with_roas = [c for c in comparisons if c['metrics'].get('roas', 0) > 0]
    
    best_performer = max(comparisons_with_roas, key=lambda x: x['metrics'].get('roas', 0)) if comparisons_with_roas else None
    worst_performer = min(comparisons_with_roas, key=lambda x: x['metrics'].get('roas', 0)) if comparisons_with_roas else None
    
    return {
        'campaigns': comparisons,
        'bestPerformer': best_performer['campaignId'] if best_performer else None,
        'worstPerformer': worst_performer['campaignId'] if worst_performer else None,
        'recommendation': f"Consider reallocating budget from {worst_performer['campaignId']} to {best_performer['campaignId']}" if best_performer and worst_performer else "Insufficient data for recommendation",
        'timestamp': datetime.now().isoformat()
    }

def generate_recommendations(campaign_id):
    """Generate actionable recommendations for campaign optimization."""
    analysis = analyze_campaign_performance(campaign_id, days=7)
    trends = detect_performance_trends(campaign_id)
    
    recommendations = []
    
    # Based on performance issues
    for issue in analysis.get('issues', []):
        if 'Low CTR' in issue:
            recommendations.append({
                'priority': 'high',
                'action': 'improve_ad_copy',
                'description': 'Test new ad headlines and descriptions',
                'expectedImpact': '+15-25% CTR improvement'
            })
        elif 'Low conversion rate' in issue:
            recommendations.append({
                'priority': 'high',
                'action': 'optimize_landing_page',
                'description': 'Review and optimize landing page experience',
                'expectedImpact': '+20-30% conversion rate improvement'
            })
        elif 'ad fatigue' in issue:
            recommendations.append({
                'priority': 'medium',
                'action': 'refresh_creatives',
                'description': 'Rotate in new ad creatives',
                'expectedImpact': '+10-20% CTR recovery'
            })
    
    # Based on trends
    for trend in trends.get('detectedTrends', []):
        if trend['type'] == 'efficiency_drop':
            recommendations.append({
                'priority': 'high',
                'action': 'adjust_targeting',
                'description': 'Refine audience targeting to improve efficiency',
                'expectedImpact': '-15-25% CPA reduction'
            })
    
    # Budget recommendations
    metrics = analysis.get('aggregateMetrics', {})
    if metrics.get('roas', 0) > 3.0:
        recommendations.append({
            'priority': 'medium',
            'action': 'increase_budget',
            'description': 'Campaign performing well, consider increasing budget',
            'expectedImpact': 'Scale profitable campaign'
        })
    elif metrics.get('roas', 0) < 1.0:
        recommendations.append({
            'priority': 'high',
            'action': 'reduce_budget',
            'description': 'Campaign underperforming, reduce budget or pause',
            'expectedImpact': 'Minimize losses'
        })
    
    return {
        'campaignId': campaign_id,
        'recommendations': recommendations,
        'totalRecommendations': len(recommendations),
        'highPriority': len([r for r in recommendations if r['priority'] == 'high']),
        'timestamp': datetime.now().isoformat()
    }

def analyze_cross_platform_performance():
    """Analyze performance across Google Ads and Meta Ads."""
    # Get all campaigns from both platforms
    google_campaigns = ['goog-camp-001', 'goog-camp-002', 'goog-camp-003']
    meta_campaigns = ['meta-camp-001', 'meta-camp-002', 'meta-camp-003']
    
    google_performance = []
    meta_performance = []
    
    for campaign_id in google_campaigns:
        analysis = analyze_campaign_performance(campaign_id, days=7)
        if analysis.get('aggregateMetrics'):
            google_performance.append(analysis['aggregateMetrics'])
    
    for campaign_id in meta_campaigns:
        analysis = analyze_campaign_performance(campaign_id, days=7)
        if analysis.get('aggregateMetrics'):
            meta_performance.append(analysis['aggregateMetrics'])
    
    # Calculate platform averages
    google_avg_roas = statistics.mean([p.get('roas', 0) for p in google_performance]) if google_performance else 0
    meta_avg_roas = statistics.mean([p.get('roas', 0) for p in meta_performance]) if meta_performance else 0
    
    google_avg_cpa = statistics.mean([p.get('avgCPA', 0) for p in google_performance]) if google_performance else 0
    meta_avg_cpa = statistics.mean([p.get('avgCPA', 0) for p in meta_performance]) if meta_performance else 0
    
    return {
        'google': {
            'avgROAS': round(google_avg_roas, 2),
            'avgCPA': round(google_avg_cpa, 2),
            'campaigns': len(google_campaigns)
        },
        'meta': {
            'avgROAS': round(meta_avg_roas, 2),
            'avgCPA': round(meta_avg_cpa, 2),
            'campaigns': len(meta_campaigns)
        },
        'recommendation': 'Allocate more budget to Google Ads' if google_avg_roas > meta_avg_roas else 'Allocate more budget to Meta Ads' if meta_avg_roas > google_avg_roas else 'Maintain current allocation',
        'timestamp': datetime.now().isoformat()
    }

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
