# Quick Start Guide

Get your AI Research Assistant Agent running in 10 minutes.

## Prerequisites Check

```bash
# Check Node.js (need 18+)
node --version

# Check Python (need 3.9+)
python --version

# Check AWS CLI (need v2)
aws --version

# Check AWS credentials
aws sts get-caller-identity
```

If any are missing, install them first.

## 5-Step Deployment

### Step 1: Enable Bedrock Access (2 min)
1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock)
2. Click "Model access" in left sidebar
3. Click "Manage model access"
4. Check "Nova Pro"
5. Click "Request model access"
6. Wait for approval (usually instant)

### Step 2: Install Dependencies (1 min)
```bash
npm install
```

### Step 3: Bootstrap CDK (1 min, first time only)
```bash
npx cdk bootstrap
```

### Step 4: Deploy (5 min)
```bash
npx cdk deploy
```

Answer "y" when prompted. Wait for deployment to complete.

### Step 5: Create Agent Alias (1 min)
1. Go to [Bedrock Agents Console](https://console.aws.amazon.com/bedrock/home#/agents)
2. Click "research-assistant-agent"
3. Click "Create alias"
4. Name: "production"
5. Version: "1"
6. Click "Create"

**Save these values**:
- Agent ID: (shown in console)
- Alias ID: (shown after creation)

## Test Your Agent

### Quick Test (Console)
1. In Bedrock Agents console
2. Click your agent
3. Click "Test" tab
4. Try: "Search for information about machine learning"

### Python Test Script
```bash
python test-agent.py
```

Enter your Agent ID and Alias ID when prompted.

## Example Prompts

### Simple Tasks
```
"Search for the latest AI trends"
"Calculate the sum of numbers 1 to 100"
"Store this data with key 'test': Hello World"
```

### Autonomous Tasks
```
"Research quantum computing, analyze the findings, and store them"
"Find information about climate change, calculate statistics, and save results"
"Search for AI ethics guidelines, summarize key points, and store the summary"
```

## Verify It's Working

You should see:
- ✅ Agent responds to prompts
- ✅ Tools are invoked (check CloudWatch logs)
- ✅ Data appears in S3 bucket
- ✅ Multi-step tasks complete autonomously

## Troubleshooting

### "Model not found"
→ Enable Nova Pro in Bedrock console (Step 1)

### "Agent not found"
→ Wait 1-2 minutes after deployment

### "Permission denied"
→ Check AWS credentials: `aws sts get-caller-identity`

### "Deployment failed"
→ Check you have permissions to create resources

## Next Steps

1. ✅ Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
2. ✅ Read [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for demonstration guide
3. ✅ Read [REQUIREMENTS_COMPLIANCE.md](REQUIREMENTS_COMPLIANCE.md) for competition compliance
4. ✅ Customize the agent for your use case

## Clean Up

When done testing:
```bash
npx cdk destroy
```

This removes all resources and stops charges.

## Cost Estimate

Testing costs (1 hour): < $1
Daily usage (moderate): $0.50 - $2
Monthly (moderate): $5 - $20

## Support

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guide
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Review CloudWatch logs for debugging
- Check AWS Bedrock documentation

## Success!

If you can run autonomous multi-step tasks, you're all set! The agent is:
- ✅ Using AWS Bedrock Nova for reasoning
- ✅ Operating autonomously
- ✅ Integrating multiple tools
- ✅ Production-ready

Enjoy your AI agent! 🚀
