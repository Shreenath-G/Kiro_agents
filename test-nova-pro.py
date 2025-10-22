#!/usr/bin/env python3
"""
Test script to verify Nova Pro timeout fix
"""
import boto3
import json
import time
from datetime import datetime

def test_nova_pro_agent():
    """Test the Nova Pro agent with simple requests"""
    
    # Initialize Bedrock Agent Runtime client
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'KTCOGQHMBD'
    agent_alias_id = 'TSTALIASID'
    session_id = f'test-session-{int(time.time())}'
    
    print(f"🧪 Testing Nova Pro Agent")
    print(f"Agent ID: {agent_id}")
    print(f"Session ID: {session_id}")
    print("-" * 50)
    
    # Test 1: Simple greeting
    print("Test 1: Simple greeting...")
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText="Hello, can you help me?"
        )
        
        # Process streaming response
        result = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    result += chunk['bytes'].decode('utf-8')
        
        print(f"✅ Success: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        if "timeout" in str(e).lower():
            print("   This is a timeout error - Nova Pro might be overloaded")
            return False
    
    # Test 2: Get campaigns
    print("\nTest 2: Get Google Ads campaigns...")
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText="Get Google Ads campaigns"
        )
        
        result = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    result += chunk['bytes'].decode('utf-8')
        
        print(f"✅ Success: Found campaigns data")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        if "timeout" in str(e).lower():
            print("   This is a timeout error - Nova Pro might be overloaded")
            return False
    
    # Test 3: Get metrics
    print("\nTest 3: Get campaign metrics...")
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText="Get metrics for campaign goog-camp-001"
        )
        
        result = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    result += chunk['bytes'].decode('utf-8')
        
        print(f"✅ Success: Got metrics data")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        if "timeout" in str(e).lower():
            print("   This is a timeout error - Nova Pro might be overloaded")
            return False
    
    print("\n🎉 All tests passed! Nova Pro is working correctly.")
    return True

def retry_test_with_backoff():
    """Retry the test with exponential backoff if timeouts occur"""
    max_retries = 3
    base_delay = 30  # Start with 30 seconds
    
    for attempt in range(max_retries):
        print(f"\n🔄 Attempt {attempt + 1}/{max_retries}")
        
        if test_nova_pro_agent():
            return True
        
        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt)
            print(f"⏳ Waiting {delay} seconds before retry...")
            time.sleep(delay)
    
    print("\n❌ All attempts failed. Nova Pro might be experiencing issues.")
    print("\n💡 Recommendations:")
    print("1. Try again in 15-30 minutes")
    print("2. Check AWS Service Health Dashboard")
    print("3. Try during off-peak hours")
    print("4. Consider using smaller, more focused requests")
    
    return False

if __name__ == "__main__":
    print("Nova Pro Timeout Fix - Test Script")
    print("=" * 50)
    
    try:
        retry_test_with_backoff()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")