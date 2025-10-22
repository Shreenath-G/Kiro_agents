#!/usr/bin/env python3
import boto3
import json

def test_analytics_function():
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Test event that mimics what Bedrock Agent sends
    test_event = {
        "messageVersion": "1.0",
        "parameters": [
            {"name": "startDate", "type": "string", "value": "2024-10-01"},
            {"name": "endDate", "type": "string", "value": "2024-10-22"}
        ],
        "sessionAttributes": {},
        "promptSessionAttributes": {},
        "sessionId": "test-session",
        "agent": {
            "name": "ad-optimizer-agent",
            "version": "DRAFT",
            "id": "KTCOGQHMBD",
            "alias": "TSTALIASID"
        },
        "actionGroup": "analytics",
        "httpMethod": "GET",
        "apiPath": "/analytics",
        "inputText": "Show me my advertising performance"
    }
    
    try:
        response = lambda_client.invoke(
            FunctionName='AdOptimizerAgentStack-AnalyticsFunctionFF8C31E8-MYsYPRwnBwcG',
            Payload=json.dumps(test_event)
        )
        
        result = json.loads(response['Payload'].read())
        print("Lambda function response:")
        print(json.dumps(result, indent=2))
        
        return result
        
    except Exception as e:
        print(f"Error testing Lambda function: {e}")
        return None

if __name__ == "__main__":
    test_analytics_function()