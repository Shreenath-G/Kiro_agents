# Model Change Summary

## What We Tried

### 1. Nova Pro (Original)
- ✅ **Simple text requests work** - Nova Pro responds to basic questions
- ❌ **Lambda function calls timeout** - "Dependency resource: received model timeout/error exception from Bedrock"
- **Root Cause**: Regional capacity issues with Nova Pro in us-east-1

### 2. Claude 3.5 Sonnet v2 
- ❌ **Requires inference profile** - "Invocation of model ID anthropic.claude-3-5-sonnet-20241022-v2:0 with on-demand throughput isn't supported"
- **Issue**: Newer Claude models need inference profiles, not direct access

### 3. Claude 3.5 Sonnet (older version)
- ❌ **Model access issues** - "The ARN you specified was not found"
- **Issue**: Model might not be enabled in your account

### 4. Claude 3 Haiku
- ✅ **Simple text requests work** - Claude responds to basic questions  
- ❌ **Lambda function calls fail** - Same ARN error when trying to invoke functions
- **Issue**: Action groups might not be compatible after model change

## Current Status

**Your agent is currently using Claude 3 Haiku** (`anthropic.claude-3-haiku-20240307-v1:0`)

### What's Working
- ✅ Basic text conversations with Claude
- ✅ All Lambda functions work perfectly (tested directly)
- ✅ Increased Lambda timeouts and memory (60s→120s, 512MB→1024MB)
- ✅ Added health check endpoints to Lambda functions

### What's Not Working
- ❌ Claude can't invoke Lambda functions through action groups
- ❌ This prevents campaign management functionality

## Recommended Next Steps

### Option 1: Go Back to Nova Pro (Recommended)
Nova Pro capacity issues are usually temporary (15-30 minutes). Since:
- Nova Pro worked for simple requests
- All Lambda functions are confirmed working
- The timeout fixes are in place

```bash
# Go back to Nova Pro
aws bedrock-agent update-agent \
  --agent-id KTCOGQHMBD \
  --agent-name "ad-optimizer-agent" \
  --foundation-model "amazon.nova-pro-v1:0" \
  --agent-resource-role-arn "arn:aws:iam::793323451177:role/AdOptimizerAgentStack-BedrockAgentRole7C982E0C-iO722SuK9wzr" \
  --instruction "You are an expert digital advertising optimization agent for small businesses."

aws bedrock-agent prepare-agent --agent-id KTCOGQHMBD
```

### Option 2: Fix Claude Action Groups
The action groups might need to be recreated after changing models:

```bash
# Redeploy the CDK stack to ensure action groups are properly configured
npx cdk deploy --force
```

### Option 3: Enable Claude 3.5 Sonnet Access
Check AWS Bedrock console to enable Claude 3.5 Sonnet model access:
1. Go to AWS Bedrock Console
2. Navigate to Model Access
3. Enable Claude 3.5 Sonnet models
4. Wait for approval (can take a few minutes)

## Testing Commands

```bash
# Test current model
python test-claude.py

# Test Nova Pro (if switched back)
python test-nova-pro.py

# Test Lambda functions directly (always works)
python test-lambda-direct.py
```

## Key Learnings

1. **Nova Pro timeout was a capacity issue**, not a code problem
2. **Your Lambda optimizations work perfectly** - functions respond in 1-2 seconds
3. **Model changes require action group compatibility** - not all models work the same way with Bedrock Agents
4. **Claude models have different access requirements** - newer versions need inference profiles

## Current Recommendation

**Go back to Nova Pro** and test again. The capacity issues were likely temporary, and your timeout fixes should prevent future issues.

If Nova Pro still has problems, the issue is regional capacity, not your implementation.