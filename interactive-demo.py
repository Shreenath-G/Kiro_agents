#!/usr/bin/env python3
"""
Interactive demo client for the AI Advertisement Optimization Agent.
Provides a chat-like interface to interact with the agent.
"""

import boto3
import json
import time
import sys
from datetime import datetime

class AgentClient:
    def __init__(self, agent_id, agent_alias_id):
        self.client = boto3.client('bedrock-agent-runtime')
        self.agent_id = agent_id
        self.agent_alias_id = agent_alias_id
        self.session_id = f"session-{int(time.time())}"
        
    def invoke(self, prompt):
        """Invoke the agent with a prompt and stream the response."""
        print(f"\n{'='*70}")
        print(f"🤖 Agent is analyzing...")
        print(f"{'='*70}\n")
        
        try:
            response = self.client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=self.session_id,
                inputText=prompt
            )
            
            # Process streaming response
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
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return None

def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print("🎯 AI Advertisement Optimization Agent - Interactive Demo")
    print("="*70)
    print("\nThis agent can:")
    print("  • Monitor and optimize Google Ads and Meta Ads campaigns")
    print("  • Analyze performance and detect trends")
    print("  • Automatically adjust bids and budgets")
    print("  • Optimize budget allocation across campaigns")
    print("  • Test ad creatives and scale winners")
    print("  • Provide actionable insights and recommendations")
    print("\n" + "="*70 + "\n")

def print_examples():
    """Print example prompts."""
    print("\n📝 Example Prompts:")
    print("-" * 70)
    print("\n1. Campaign Overview:")
    print("   'Show me all my campaigns and their performance'")
    print("\n2. Performance Analysis:")
    print("   'Analyze campaign goog-camp-001 and identify any issues'")
    print("\n3. Budget Optimization:")
    print("   'Optimize my $5000 monthly budget across all campaigns'")
    print("\n4. Autonomous Optimization:")
    print("   'Find my worst performing campaign and take action to improve it'")
    print("\n5. Cross-Platform Analysis:")
    print("   'Compare Google Ads vs Meta Ads performance'")
    print("\n6. Creative Testing:")
    print("   'Which campaign needs new ad creatives? Set up an A/B test'")
    print("\n7. Trend Detection:")
    print("   'Are any of my campaigns showing signs of ad fatigue?'")
    print("\n8. Budget Reallocation:")
    print("   'Reallocate budget from underperformers to top performers'")
    print("\n" + "-"*70 + "\n")

def main():
    print_banner()
    
    # Get agent configuration
    print("📋 Configuration:")
    agent_id = input("Enter your Agent ID: ").strip()
    agent_alias_id = input("Enter your Agent Alias ID (or press Enter for 'TSTALIASID'): ").strip() or "TSTALIASID"
    
    if not agent_id:
        print("\n❌ Agent ID is required!")
        sys.exit(1)
    
    # Create client
    client = AgentClient(agent_id, agent_alias_id)
    print(f"\n✅ Connected to agent: {agent_id}")
    print(f"   Session ID: {client.session_id}")
    
    # Show examples
    show_examples = input("\nShow example prompts? (y/n): ").strip().lower()
    if show_examples == 'y':
        print_examples()
    
    # Interactive loop
    print("\n💬 Chat with the agent (type 'quit' to exit, 'examples' for prompts, 'help' for commands)")
    print("="*70 + "\n")
    
    while True:
        try:
            # Get user input
            prompt = input("You: ").strip()
            
            if not prompt:
                continue
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if prompt.lower() == 'examples':
                print_examples()
                continue
            
            if prompt.lower() == 'help':
                print("\n📚 Available Commands:")
                print("  quit/exit/q  - Exit the demo")
                print("  examples     - Show example prompts")
                print("  clear        - Start new session")
                print("  help         - Show this help message")
                print()
                continue
            
            if prompt.lower() == 'clear':
                # Start new session
                client.session_id = f"session-{int(time.time())}"
                print(f"\n✅ Started new session: {client.session_id}\n")
                continue
            
            # Invoke agent
            start_time = time.time()
            response = client.invoke(prompt)
            elapsed = time.time() - start_time
            
            if response:
                print(f"⏱️  Response time: {elapsed:.2f}s\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
