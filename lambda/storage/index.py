import json
import os
import boto3
from datetime import datetime
from decimal import Decimal

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = os.environ.get('BUCKET_NAME')
METRICS_TABLE = os.environ.get('METRICS_TABLE')

def handler(event, context):
    """
    Storage tool for the AI agent.
    Stores and retrieves campaign insights, decisions, and performance history.
    """
    print(f"Received event: {json.dumps(event)}")
    
    api_path = event.get('apiPath', '')
    http_method = event.get('httpMethod', '')
    request_body = event.get('requestBody', {})
    parameters = event.get('parameters', [])
    
    # Handle STORE operation
    if http_method == 'POST' and '/store' in api_path:
        # Extract data from request body
        content = request_body.get('content', {})
        body_str = content.get('application/json', '')
        
        if not body_str:
            return error_response(event, 'Request body is required')
        
        try:
            body_data = json.loads(body_str)
            key = body_data.get('key')
            data = body_data.get('data')
            
            if not key or not data:
                return error_response(event, 'Both key and data are required')
            
            # Store in S3
            s3_key = f"insights/{key}.json"
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=json.dumps({
                    'data': data,
                    'timestamp': datetime.now().isoformat(),
                    'key': key,
                    'type': 'campaign_insight'
                }),
                ContentType='application/json',
                Metadata={
                    'timestamp': datetime.now().isoformat(),
                    'key': key
                }
            )
            
            return success_response(event, {
                'message': 'Campaign insight stored successfully',
                'key': key,
                's3_key': s3_key,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return error_response(event, f'Error storing data: {str(e)}')
    
    # Handle RETRIEVE operation
    elif http_method == 'GET' and '/retrieve' in api_path:
        # Extract key from parameters
        key = None
        for param in parameters:
            if param.get('name') == 'key':
                key = param.get('value')
                break
        
        if not key:
            return error_response(event, 'Key parameter is required')
        
        try:
            # Retrieve from S3
            s3_key = f"insights/{key}.json"
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            data = json.loads(response['Body'].read().decode('utf-8'))
            
            return success_response(event, {
                'message': 'Campaign insight retrieved successfully',
                'data': data,
                'timestamp': datetime.now().isoformat()
            })
            
        except s3_client.exceptions.NoSuchKey:
            return error_response(event, f'No data found for key: {key}')
        except Exception as e:
            return error_response(event, f'Error retrieving data: {str(e)}')
    
    else:
        return error_response(event, 'Invalid operation')

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
                    'body': json.dumps(data)
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
