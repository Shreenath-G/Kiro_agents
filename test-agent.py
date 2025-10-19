#!/usr/bin/env python3
"""
Test client for the AI Advertisement Optimization Agent.
Demonstrates autonomous campaign optimization capabilities.
"""

import boto3
import json
import time
import sys

def invoke_agent(agent_id, agent_alias_id, session_id, prompt):
    """Invoke the Bedrock agent with a prompt."""
    client = boto3.client('bedrock-agent-runtime')
    
    print(f"\n{'='*70}")
    print(f"USER: {prompt}")
    print(f"{'='*70}\n")
    
    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=prompt
    )
    
    # Process the streaming response
    event_stream = response['completion']
    full_response = ""
    
    for event in event_stream:
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                text = chunk['bytes'].decode('utf-8')
                full_response += text
                print(text, end='', flush=True)
    
    print(f"\n\n{'='*70}\n")
    return full_response

def main():
    # Configuration - Update these after deployment
    AGENT_ID = input("Enter your Agent ID: ").strip()
    AGENT_ALIAS_ID = input("Enter your Agent Alias ID (or press Enter for 'TSTALIASID'): ").strip() or "TSTALIASID"
    SESSION_ID = f"test-session-{int(time.time())}"
    
    print("\n🤖 AI Advertisement Optimization Agent - Test Client")
    print("=" * 70)
    
    # Test 1: Get campaign overview
    print("\n📋 Test 1: Get Campaign Overview")
    invoke_agent(
        AGENT_ID,
        AGENT_ALIAS_ID,
        SESSION_ID,
        "Show me all my Google Ads and Meta Ads campaigns with their current performance."
    )
    
    time.sleep(2)
    
    # Test 2: Analyze specific campaign
    print("\n📋 Test 2: Analyze Campaign Performance")
    invoke_agent(
        AGENT_ID,
        AGENT_ALIAS_ID,
        SESSION_ID,
        "Analyze the performance of campaign goog-camp-001 and tell me if there are any issues."
    )
    
    time.sleep(2)
    
    # Test 3: Budget optimization
    print("\n📋 Test 3: Budget Optimization")
    invoke_agent(
        AGENT_ID,
        AGENT_ALIAS_ID,
        SESSION_ID,
        "I have a total budget of $5000 per month. Optimize the budget allocation across all my campaigns to maximize ROAS."
    )
    
    time.sleep(2)
    
    # Test 4: Autonomous optimization (multi-step)
    print("\n📋 Test 4: Autonomous Multi-Step Optimization")
    invoke_agent(
        AGENT_ID,
        AGENT_ALIAS_ID,
        SESSION_ID,
        """Analyze all my campaigns, identify the worst performer, and take action to improve it. 
        If a campaign is underperforming significantly, reduce its budget and reallocate to better performers. 
        Store your decision and reasoning for future reference."""
    )
    
    time.sleep(2)
    
    # Test 5: Cross-platform analysis
    print("\n📋 Test 5: Cross-Platform Analysis")
    invoke_agent(
        AGENT_ID,
        AGENT_ALIAS_ID,
        SESSION_ID,
        "Compare the performance of Google Ads vs Meta Ads. Which platform is giving me better ROI?"
    )
    
    time.sleep(2)
    
    # Test 6: Creative testing
    print("\n📋 Test 6: Creative Testing Recommendation")
    invoke_agent(
        AGENT_ID,
        AGENT_ALIAS_ID,
        SESSION_ID,
        "Which of my Meta campaigns would benefit most from A/B testing new creatives? Set up a test for that campaign."
    )
    
    print("\n✅ All tests completed!")
    print("\n📊 Summary:")
    print("- Campaign overview retrieved")
    print("- Performance analysis completed")
    print("- Budget optimization calculated")
    print("- Autonomous optimization executed")
    print("- Cross-platform comparison done")
    print("- Creative testing initiated")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
