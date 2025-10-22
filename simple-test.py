#!/usr/bin/env python3
import boto3
import time

AGENT_ID = "KTCOGQHMBD"
AGENT_ALIAS_ID = "TSTALIASID"
SESSION_ID = f"test-{int(time.time())}"

client = boto3.client('bedrock-agent-runtime')

print("Testing agent with simple prompt...")
print("=" * 70)

try:
    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=SESSION_ID,
        inputText="Hello, can you help me?"
    )
    
    event_stream = response['completion']
    for event in event_stream:
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                text = chunk['bytes'].decode('utf-8')
                print(text, end='', flush=True)
    
    print("\n" + "=" * 70)
    print("✅ Success! Agent is working.")
    
except Exception as e:
    print(f"❌ Error: {e}")
