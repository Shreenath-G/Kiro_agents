# Demo Script for AI Research Assistant Agent

This script provides a step-by-step demonstration of the agent's capabilities.

## Pre-Demo Setup

1. Deploy the agent: `npx cdk deploy`
2. Create agent alias in AWS Console
3. Note Agent ID and Alias ID
4. Have AWS Console open to Bedrock Agents

## Demo Flow (15 minutes)

### Part 1: Introduction (2 minutes)

**Script**:
"Today I'll demonstrate an autonomous AI agent built entirely on AWS. This agent uses Amazon Bedrock's Nova Pro model for reasoning and can independently research topics, execute code, and manage its own knowledge base."

**Show**:
- Architecture diagram from ARCHITECTURE.md
- AWS Console with deployed resources

### Part 2: Simple Tool Usage (3 minutes)

**Test 1: Web Search**
```
Prompt: "Search for the latest developments in quantum computing"
```

**Expected Behavior**:
- Agent uses web_search tool
- Returns structured results
- Shows autonomous tool selection

**Talking Points**:
- Agent decided to use web search without being told
- Demonstrates reasoning about which tool to use
- Results stored automatically in S3

**Test 2: Code Execution**
```
Prompt: "Calculate the factorial of 10 using Python"
```

**Expected Behavior**:
- Agent uses execute_code tool
- Writes and runs Python code
- Returns result: 3,628,800

**Talking Points**:
- Agent can write and execute code
- Safe sandboxed environment
- Useful for data analysis and calculations

### Part 3: Autonomous Multi-Step Task (5 minutes)

**Test 3: Complex Research Task**
```
Prompt: "Research artificial intelligence applications in healthcare, 
analyze the top 3 use cases, calculate their potential impact scores 
(on a scale of 1-10), and store your findings with the key 'ai-healthcare-analysis'"
```

**Expected Behavior**:
1. Agent reasons about the task
2. Uses web_search to find information
3. Uses execute_code to analyze and score
4. Uses storage to persist findings
5. Confirms completion

**Talking Points**:
- No human intervention between steps
- Agent chains multiple tools autonomously
- Demonstrates true autonomous behavior
- Makes decisions about tool usage and sequencing

**Show in Console**:
- CloudWatch logs showing tool invocations
- S3 bucket with stored research
- Agent reasoning in Bedrock console

### Part 4: Knowledge Retrieval (2 minutes)

**Test 4: Retrieve Previous Work**
```
Prompt: "Retrieve the ai-healthcare-analysis you stored earlier and summarize it"
```

**Expected Behavior**:
- Agent uses storage retrieval
- Accesses previously stored data
- Provides summary

**Talking Points**:
- Agent maintains its own knowledge base
- Can build on previous work
- Demonstrates memory and context

### Part 5: Technical Deep Dive (3 minutes)

**Show Code**:
1. Agent configuration in `lib/ai-agent-stack.ts`
   - Nova Pro model selection
   - Reasoning instructions
   - Action group setup

2. Lambda function example (`lambda/storage/index.py`)
   - Tool implementation
   - S3 integration
   - Response formatting

3. Infrastructure as Code
   - CDK deployment
   - Security (IAM roles)
   - Scalability (serverless)

**Talking Points**:
- Production-ready infrastructure
- Security best practices
- Easy to extend with new tools
- Fully automated deployment

## Q&A Preparation

### Expected Questions

**Q: How does the agent decide which tool to use?**
A: The Nova Pro model uses its reasoning capabilities to understand the task requirements and select appropriate tools based on the OpenAPI specifications we provide for each action group.

**Q: Can you add more tools?**
A: Yes, easily. Just create a new Lambda function, define its OpenAPI spec, and add it as an action group. The agent will automatically learn to use it.

**Q: How does this handle errors?**
A: The agent can retry operations, and each Lambda function has error handling. The agent's reasoning allows it to adjust its approach if a tool fails.

**Q: What about security?**
A: We use IAM roles with least privilege, sandboxed code execution, encrypted S3 storage, and no hardcoded credentials.

**Q: How much does this cost?**
A: For moderate usage, approximately $5-20/month. Bedrock charges per token, Lambda per invocation, and S3 per GB stored.

**Q: Can this scale?**
A: Yes, it's fully serverless. Lambda auto-scales, Bedrock is managed, and S3 handles unlimited storage.

## Demo Tips

1. **Have backup**: Pre-run tests and save outputs in case of live demo issues
2. **Show logs**: CloudWatch logs demonstrate actual tool invocations
3. **Emphasize autonomy**: Highlight that agent makes decisions independently
4. **Show S3 contents**: Proves data is actually being stored
5. **Explain reasoning**: Walk through how agent thinks about tasks

## Backup Demos

If live demo fails, show:
1. Pre-recorded video of agent interaction
2. CloudWatch logs from previous successful runs
3. S3 bucket contents showing stored research
4. Code walkthrough with explanation

## Post-Demo

**Provide**:
- GitHub repository link
- Deployment instructions
- Architecture documentation
- Cost estimates

**Highlight**:
- Meets all competition requirements
- Production-ready
- Extensible architecture
- Comprehensive documentation

## Success Metrics

Demo is successful if audience understands:
1. ✅ Agent uses AWS Bedrock Nova for reasoning
2. ✅ Agent operates autonomously
3. ✅ Agent integrates multiple tools
4. ✅ Solution is production-ready
5. ✅ Architecture is scalable and secure

## Time Allocation

- Introduction: 2 min
- Simple tools: 3 min
- Autonomous task: 5 min
- Knowledge retrieval: 2 min
- Technical dive: 3 min
- Q&A: Remaining time

Total: 15 minutes + Q&A
