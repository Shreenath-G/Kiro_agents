#!/usr/bin/env python3
import boto3
import json
import time

def test_agent():
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    agent_id = 'KTCOGQHMBD'
    agent_alias_id = 'TSTALIASID'  # Default test alias
    
    try:
        print("Testing agent with simple query...")
        
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId='test-session-' + str(int(time.time())),
            inputText="Hello, can you help me with my advertising campaigns?"
        )
        
        print("Response received!")
        
        # Process the response stream
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    text = chunk['bytes'].decode('utf-8')
                    print(f"Agent: {text}")
                    
    except Exception as e:
        print(f"Error: {e}")
        print("This might be normal - the agent might not have a test alias yet.")
        print("Try testing in the AWS Console instead.")

if __name__ == "__main__":
    test_agent()