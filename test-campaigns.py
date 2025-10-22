#!/usr/bin/env python3
import boto3
import time

AGENT_ID = "KTCOGQHMBD"
AGENT_ALIAS_ID = "TSTALIASID"

def test_agent(prompt, test_name):
    """Test the agent with a specific prompt."""
    SESSION_ID = f"test-{int(time.time())}"
    client = boto3.client('bedrock-agent-runtime')
    
    print(f"\n{'='*70}")
    print(f"🧪 {test_name}")
    print(f"{'='*70}")
    print(f"USER: {prompt}")
    print(f"{'='*70}\n")
    
    try:
        response = client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=SESSION_ID,
            inputText=prompt
        )
        
        event_stream = response['completion']
        for event in event_stream:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    text = chunk['bytes'].decode('utf-8')
                    print(text, end='', flush=True)
        
        print(f"\n{'='*70}\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

# Run tests
print("🤖 AI Advertisement Optimization Agent - Campaign Tests")
print("="*70)

tests = [
    ("Show me my Google Ads campaigns", "Test 1: Get Google Campaigns"),
    ("Show me my Meta Ads campaigns", "Test 2: Get Meta Campaigns"),
    ("Get analytics for the last 7 days", "Test 3: Get Analytics"),
    ("Optimize my budget allocation", "Test 4: Budget Optimization"),
]

passed = 0
for prompt, name in tests:
    if test_agent(prompt, name):
        passed += 1
    time.sleep(2)  # Brief pause between tests

print(f"\n✅ Tests completed: {passed}/{len(tests)} passed")
