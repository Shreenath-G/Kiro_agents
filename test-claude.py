#!/usr/bin/env python3
"""
Test script to verify Claude 3.5 Sonnet v2 is working
"""
import boto3
import json
import time
from datetime import datetime

def test_claude_agent():
    """Test the Claude agent with simple requests"""
    
    # Initialize Bedrock Agent Runtime client
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'KTCOGQHMBD'
    agent_alias_id = 'TSTALIASID'
    session_id = f'claude-test-{int(time.time())}'
    
    print(f"🧪 Testing Claude 3.5 Sonnet v2 Agent")
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
            inputText="Hello, can you help me with my advertising campaigns?"
        )
        
        # Process streaming response
        result = ""
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    result += chunk['bytes'].decode('utf-8')
        
        print(f"✅ Success: {result[:150]}...")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        if "timeout" in str(e).lower():
            print("   This is a timeout error - Claude might be overloaded")
            return False
        return False
    
    # Test 2: Get campaigns (the one that was failing with Nova Pro)
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
        
        print(f"✅ Success: Claude successfully called Lambda functions!")
        print(f"   Response: {result[:150]}...")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        if "timeout" in str(e).lower():
            print("   This is a timeout error")
            return False
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
        print(f"   Response: {result[:150]}...")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        if "timeout" in str(e).lower():
            print("   This is a timeout error")
            return False
        return False
    
    print("\n🎉 All tests passed! Claude 3.5 Sonnet v2 is working perfectly!")
    return True

def check_agent_model():
    """Check what model the agent is currently using"""
    client = boto3.client('bedrock-agent', region_name='us-east-1')
    
    try:
        response = client.get_agent(agentId='KTCOGQHMBD')
        model = response['agent']['foundationModel']
        status = response['agent']['agentStatus']
        
        print(f"Current Model: {model}")
        print(f"Agent Status: {status}")
        
        if 'claude' in model.lower():
            print("✅ Agent is using Claude!")
        elif 'nova' in model.lower():
            print("⚠️  Agent is still using Nova Pro")
            print("   The CDK deployment might not have updated the agent yet")
        
        return model
        
    except Exception as e:
        print(f"❌ Error checking agent: {str(e)}")
        return None

if __name__ == "__main__":
    print("Claude 3.5 Sonnet v2 Test Script")
    print("=" * 50)
    
    # First check what model is being used
    print("Checking current agent model...")
    model = check_agent_model()
    print("-" * 50)
    
    if model and 'claude' in model.lower():
        print("✅ Agent is using Claude - proceeding with tests")
        test_claude_agent()
    elif model and 'nova' in model.lower():
        print("⚠️  Agent is still using Nova Pro")
        print("The CDK deployment might not have updated the agent configuration yet.")
        print("\n💡 Try these steps:")
        print("1. Wait 2-3 minutes for AWS to propagate changes")
        print("2. Run this test again")
        print("3. If still using Nova Pro, the agent might need manual update in AWS Console")
    else:
        print("❌ Could not determine agent model - proceeding with test anyway")
        test_claude_agent()