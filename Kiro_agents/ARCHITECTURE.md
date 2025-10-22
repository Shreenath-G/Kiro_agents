# Architecture Documentation

## Overview

This AI Research Assistant Agent demonstrates a complete autonomous AI system built on AWS that meets all competition requirements.

## Requirements Compliance

### 1. LLM Hosted on AWS ✅
- **Service**: Amazon Bedrock
- **Model**: amazon.nova-pro-v1:0 (Nova Pro)
- **Reasoning**: Nova Pro provides advanced reasoning capabilities for autonomous decision-making

### 2. AWS Services Used ✅

#### Core Services:
- **Amazon Bedrock Agents**: Primary agent framework with action groups
- **Amazon Bedrock/Nova**: LLM for reasoning and decision-making
- **AWS Lambda**: Executes agent tools (3 functions)
- **Amazon S3**: Knowledge base and results storage
- **IAM**: Security and permissions management

#### Infrastructure:
- **AWS CDK**: Infrastructure as Code for deployment
- **CloudFormation**: Underlying deployment mechanism

### 3. AI Agent Qualifications ✅

#### Uses Reasoning LLMs:
- Nova Pro model provides multi-step reasoning
- Agent instruction includes explicit reasoning directives
- Breaks down complex tasks autonomously

#### Demonstrates Autonomous Capabilities:
- Can execute multi-step tasks without human intervention
- Makes decisions about which tools to use
- Synthesizes information from multiple sources
- Stores and retrieves its own research findings

#### Integrates External Tools:
- **Web Search**: Searches for information (simulated, can integrate real APIs)
- **Code Execution**: Runs Python code for calculations
- **Storage**: Persists and retrieves data from S3
- **Multi-tool orchestration**: Combines tools to complete complex tasks

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User/Client                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Amazon Bedrock Agent Runtime                    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Research Assistant Agent                    │    │
│  │         (amazon.nova-pro-v1:0)                     │    │
│  │                                                     │    │
│  │  - Reasoning & Decision Making                     │    │
│  │  - Task Decomposition                              │    │
│  │  - Tool Selection & Orchestration                  │    │
│  └────────────────────────────────────────────────────┘    │
└───────┬──────────────────┬──────────────────┬───────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Action Group │  │ Action Group │  │ Action Group │
│ Web Search   │  │ Code Execute │  │   Storage    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       ▼                 ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Lambda     │  │   Lambda     │  │   Lambda     │
│ Web Search   │  │ Code Exec    │  │  Storage     │
└──────┬───────┘  └──────────────┘  └──────┬───────┘
       │                                    │
       └────────────────┬───────────────────┘
                        ▼
                ┌──────────────┐
                │   Amazon S3  │
                │  Knowledge   │
                │    Bucket    │
                └──────────────┘
```

## Component Details

### 1. Bedrock Agent
- **Foundation Model**: Nova Pro (reasoning-capable)
- **Instruction**: Detailed system prompt for autonomous behavior
- **Session Management**: Maintains context across interactions
- **Action Groups**: Three tool integrations

### 2. Action Groups

#### Web Search Action Group
- **Purpose**: Information retrieval
- **API**: OpenAPI 3.0 specification
- **Lambda**: web-search function
- **Capabilities**: 
  - Search queries
  - Result ranking
  - Automatic storage in S3

#### Code Execution Action Group
- **Purpose**: Data analysis and calculations
- **API**: OpenAPI 3.0 specification
- **Lambda**: code-execution function
- **Capabilities**:
  - Safe Python execution
  - Variable capture
  - Output streaming

#### Storage Action Group
- **Purpose**: Knowledge persistence
- **API**: OpenAPI 3.0 specification
- **Lambda**: storage function
- **Capabilities**:
  - Store research findings
  - Retrieve previous work
  - Timestamped versioning

### 3. Lambda Functions

All functions use Python 3.12 runtime and follow Bedrock Agent integration patterns.

#### Web Search Function
```python
Input: { "query": "search term" }
Output: { "results": [...], "total_results": N }
```

#### Code Execution Function
```python
Input: { "code": "python code" }
Output: { "success": bool, "output": "...", "variables": {...} }
```

#### Storage Function
```python
Store: { "key": "...", "data": "..." }
Retrieve: { "key": "..." }
```

### 4. S3 Bucket
- **Purpose**: Knowledge base and results storage
- **Structure**:
  - `/research/` - Stored research findings
  - `/searches/` - Search history and results
- **Features**:
  - Versioning enabled
  - Encryption at rest
  - Lifecycle policies (optional)

## Autonomous Behavior

The agent demonstrates autonomy through:

1. **Task Decomposition**: Breaks complex requests into steps
2. **Tool Selection**: Chooses appropriate tools without prompting
3. **Multi-step Execution**: Chains multiple tool calls
4. **Self-correction**: Can retry or adjust approach
5. **Knowledge Management**: Stores and retrieves its own findings

## Example Autonomous Flow

```
User: "Research AI in healthcare, analyze the data, and store findings"

Agent Reasoning:
1. Need to search for information → Use web_search
2. Got results, need to analyze → Use execute_code
3. Have insights, need to persist → Use storage
4. Task complete, summarize for user

Execution:
1. web_search("AI in healthcare")
2. execute_code("# analyze search results...")
3. storage.store("ai-healthcare", "findings...")
4. Return summary to user
```

## Security

- IAM roles with least privilege
- Lambda execution roles scoped to specific resources
- S3 bucket encryption
- No hardcoded credentials
- Sandboxed code execution

## Scalability

- Lambda auto-scaling
- S3 unlimited storage
- Bedrock managed service
- Stateless design

## Cost Optimization

- Lambda pay-per-use
- S3 lifecycle policies
- Bedrock on-demand pricing
- No idle resources

## Monitoring

- CloudWatch Logs for all Lambda functions
- Bedrock Agent metrics
- S3 access logs
- X-Ray tracing (optional)
