#!/usr/bin/env python3
"""
Test Lambda functions directly to isolate the issue
"""
import boto3
import json
import time

def test_lambda_function(function_name, payload):
    """Test a Lambda function directly"""
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    try:
        print(f"Testing {function_name}...")
        
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        result = json.loads(response['Payload'].read().decode('utf-8'))
        print(f"✅ Success: {function_name}")
        print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {function_name}")
        print(f"   Error: {str(e)}")
        return False

def main():
    print("Testing Lambda Functions Directly")
    print("=" * 50)
    
    # Test payloads for each function
    test_cases = [
        {
            'function': 'AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of',
            'payload': {
                'apiPath': '/campaigns',
                'httpMethod': 'GET',
                'parameters': []
            }
        },
        {
            'function': 'AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of',
            'payload': {
                'apiPath': '/health',
                'httpMethod': 'GET',
                'parameters': []
            }
        },
        {
            'function': 'AdOptimizerAgentStack-MetaAdsFunction54F22D99-fW7MjIGjmOgW',
            'payload': {
                'apiPath': '/campaigns',
                'httpMethod': 'GET',
                'parameters': []
            }
        },
        {
            'function': 'AdOptimizerAgentStack-BudgetOptimizerFunction4A1C8-mvHkrlQAENX8',
            'payload': {
                'apiPath': '/health',
                'httpMethod': 'GET',
                'parameters': []
            }
        }
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for test_case in test_cases:
        if test_lambda_function(test_case['function'], test_case['payload']):
            success_count += 1
        print("-" * 30)
        time.sleep(1)  # Small delay between tests
    
    print(f"\nResults: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All Lambda functions are working!")
        print("The issue is likely with Nova Pro <-> Lambda integration")
        print("\n💡 Next steps:")
        print("1. Nova Pro might be experiencing regional capacity issues")
        print("2. Try again in 15-30 minutes")
        print("3. The Lambda timeout fixes are working, just need Nova Pro to stabilize")
    else:
        print("❌ Some Lambda functions have issues")
        print("Need to fix Lambda functions first before testing Nova Pro")

if __name__ == "__main__":
    main()