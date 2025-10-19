# Deployment Guide

## Prerequisites

### 1. AWS Account Setup
- Active AWS account
- Bedrock access enabled in your region
- Nova model access granted (request if needed)

### 2. Local Environment
```bash
# Required tools
- Node.js 18+ and npm
- Python 3.9+
- AWS CLI v2
- Git
```

### 3. AWS CLI Configuration
```bash
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (us-east-1 recommended)
# - Output format (json)
```

### 4. Enable Bedrock Models
1. Go to AWS Console > Amazon Bedrock
2. Navigate to "Model access"
3. Request access to "Nova Pro" model
4. Wait for approval (usually instant)

## Installation Steps

### Step 1: Clone and Setup
```bash
# Navigate to project directory
cd aws-ai-research-agent

# Install Node.js dependencies
npm install
```

### Step 2: Bootstrap CDK (First Time Only)
```bash
npx cdk bootstrap
```

This creates necessary CDK resources in your AWS account.

### Step 3: Deploy Infrastructure
```bash
# Deploy the stack
npx cdk deploy

# Or use the deployment script
chmod +x deploy.sh
./deploy.sh
```

The deployment will:
- Create S3 bucket for knowledge storage
- Deploy 3 Lambda functions
- Create Bedrock Agent with Nova Pro
- Set up IAM roles and permissions
- Configure action groups

### Step 4: Create Agent Alias

After deployment, you need to create an alias:

1. Go to AWS Console > Amazon Bedrock > Agents
2. Find "research-assistant-agent"
3. Click "Create alias"
4. Name it "production" or "test"
5. Select version "1" (or latest)
6. Click "Create"

Note the Agent ID and Alias ID for testing.

## Testing

### Option 1: Python Test Script
```bash
python test-agent.py
```

Enter your Agent ID and Alias ID when prompted.

### Option 2: AWS Console
1. Go to Bedrock > Agents
2. Select your agent
3. Click "Test" tab
4. Enter prompts and interact

### Option 3: AWS CLI
```bash
aws bedrock-agent-runtime invoke-agent \
  --agent-id YOUR_AGENT_ID \
  --agent-alias-id YOUR_ALIAS_ID \
  --session-id test-session-1 \
  --input-text "Research quantum computing trends" \
  output.txt
```

## Verification

### Test 1: Simple Query
```
Prompt: "Search for information about machine learning"
Expected: Agent uses web_search tool and returns results
```

### Test 2: Code Execution
```
Prompt: "Calculate the sum of numbers from 1 to 100"
Expected: Agent uses execute_code tool and returns 5050
```

### Test 3: Storage
```
Prompt: "Store this data with key 'test': Hello World"
Expected: Agent uses storage tool and confirms storage
```

### Test 4: Autonomous Multi-Step
```
Prompt: "Research AI ethics, analyze key points, and store findings"
Expected: Agent chains web_search → execute_code → storage
```

## Troubleshooting

### Issue: "Model not found"
**Solution**: Ensure Nova Pro access is enabled in Bedrock console

### Issue: "Agent not found"
**Solution**: Wait 1-2 minutes after deployment for agent to be ready

### Issue: "Permission denied"
**Solution**: Check IAM roles have correct permissions

### Issue: "Lambda timeout"
**Solution**: Increase timeout in lib/ai-agent-stack.ts and redeploy

### Issue: "S3 access denied"
**Solution**: Verify bucket name in Lambda environment variables

## Monitoring

### CloudWatch Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/AIResearchAgentStack-WebSearchFunction --follow
aws logs tail /aws/lambda/AIResearchAgentStack-CodeExecutionFunction --follow
aws logs tail /aws/lambda/AIResearchAgentStack-StorageFunction --follow
```

### Agent Metrics
- Go to Bedrock > Agents > Your Agent > Metrics
- View invocation count, latency, errors

### S3 Contents
```bash
# List stored research
aws s3 ls s3://ai-agent-knowledge-YOUR_ACCOUNT/research/

# List search history
aws s3 ls s3://ai-agent-knowledge-YOUR_ACCOUNT/searches/
```

## Cleanup

### Remove All Resources
```bash
# Delete the stack
npx cdk destroy

# Or manually delete from CloudFormation console
```

This will remove:
- Bedrock Agent
- Lambda functions
- S3 bucket (and contents)
- IAM roles
- All associated resources

## Cost Estimate

Approximate costs for moderate usage:
- Bedrock Nova Pro: $0.008 per 1K input tokens, $0.032 per 1K output tokens
- Lambda: $0.20 per 1M requests + compute time
- S3: $0.023 per GB/month
- Data transfer: Varies

Estimated monthly cost for testing: $5-20

## Next Steps

1. Integrate real web search API (e.g., Bing, Google)
2. Add more tools (database access, email, etc.)
3. Implement knowledge base with vector search
4. Add API Gateway for external access
5. Set up CI/CD pipeline
6. Add monitoring and alerting
7. Implement rate limiting and quotas

## Support

For issues:
1. Check CloudWatch Logs
2. Review AWS Bedrock documentation
3. Check CDK deployment logs
4. Verify IAM permissions
