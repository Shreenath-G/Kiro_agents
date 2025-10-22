# Nova Pro Timeout Error - Fix Guide

## The Problem
You're getting: "Dependency resource: received model timeout/error exception from Bedrock. Try the request again."

This happens with Nova Pro when:
1. The model is temporarily overloaded (high demand)
2. Your request is complex and needs more processing time
3. Regional capacity constraints
4. Network latency issues

## Nova Pro Specific Solutions

### 1. Simple Retry (Most Common Fix)
Nova Pro timeouts are usually temporary. Just retry your request:

```bash
# If using the agent directly, just try the same request again
# The timeout is often resolved within 30-60 seconds
```

### 2. Optimize Your Requests
Break down complex requests into smaller parts:

**Instead of:**
"Analyze all campaigns, optimize budgets, and provide detailed recommendations"

**Try:**
1. "Get Google Ads campaigns"
2. "Get metrics for campaign goog-camp-001"  
3. "Optimize budget for $5000 total budget"

### 3. Increase Timeouts (Already Done)
Your stack now has increased session timeout (3600 seconds) which helps Nova Pro handle longer processing.

### 4. Use Different Nova Pro Variants
Try these Nova Pro variants if the base model times out:

```typescript
// Current (keep this):
foundationModel: 'amazon.nova-pro-v1:0',

// Alternative variants to try:
// foundationModel: 'amazon.nova-pro-v1:0:24k',    // 24k context
// foundationModel: 'amazon.nova-pro-v1:0:300k',   // 300k context
```

### 5. Check Nova Pro Status
```bash
# Check if Nova Pro is available and healthy
aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?modelId=='amazon.nova-pro-v1:0']"

# Check your region's Bedrock service status
aws bedrock get-model-invocation-logging-configuration --region us-east-1
```

## Immediate Actions

### Step 1: Redeploy with Increased Timeout
```bash
npx cdk deploy
```

### Step 2: Test with Simple Request
```bash
# Test with a basic request first
aws bedrock-agent-runtime invoke-agent \
  --agent-id YOUR_AGENT_ID \
  --agent-alias-id TSTALIASID \
  --session-id test-session-$(date +%s) \
  --input-text "Hello, can you help me?" \
  response.json

cat response.json
```

### Step 3: Gradually Increase Complexity
Once basic requests work, try:
1. "Get Google Ads campaigns"
2. "Get metrics for a specific campaign"
3. More complex optimization requests

## Nova Pro Best Practices

### 1. Request Patterns That Work Well
- Single, focused requests
- Clear, specific instructions
- Avoid very long context in one request

### 2. Request Patterns to Avoid
- Multiple complex operations in one request
- Very long instruction prompts
- Rapid successive requests (wait 2-3 seconds between calls)

### 3. Optimal Session Management
```bash
# Use unique session IDs for each conversation
SESSION_ID="session-$(date +%s)"

# Don't reuse sessions immediately after timeouts
# Wait 30-60 seconds before retrying with same session
```

## Monitoring Nova Pro Performance

### Check Request Patterns
```bash
# Monitor CloudWatch logs for your Lambda functions
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/AIAgentStack"

# Check for timeout patterns
aws logs filter-log-events \
  --log-group-name "/aws/lambda/AIAgentStack-GoogleAdsFunction" \
  --filter-pattern "timeout"
```

### Performance Optimization
1. **Lambda Memory**: Increase if needed (currently 512MB)
2. **Lambda Timeout**: Currently 60s, increase if Nova Pro needs more time
3. **Request Size**: Keep requests focused and concise

## When Nova Pro is Consistently Timing Out

### Temporary Workaround
If Nova Pro has persistent issues in your region:

1. **Wait 15-30 minutes** - Often resolves automatically
2. **Try different times of day** - Less load during off-peak hours
3. **Use smaller request batches** - Break complex operations into steps

### Check AWS Service Health
```bash
# Check AWS Service Health Dashboard
# https://status.aws.amazon.com/

# Check Bedrock service status specifically
aws support describe-services --language en
```

## Testing Your Fix

```bash
# 1. Deploy the updated stack
npx cdk deploy

# 2. Wait 2-3 minutes for deployment to complete

# 3. Test with simple request
aws bedrock-agent-runtime invoke-agent \
  --agent-id $(aws cloudformation describe-stacks --stack-name AIAgentStack --query 'Stacks[0].Outputs[?OutputKey==`AgentId`].OutputValue' --output text) \
  --agent-alias-id TSTALIASID \
  --session-id test-$(date +%s) \
  --input-text "Get Google Ads campaigns" \
  response.json

# 4. Check response
cat response.json | jq .
```

## Success Indicators

✅ **Working correctly when you see:**
- Response within 10-30 seconds
- Proper JSON response structure
- No timeout errors in CloudWatch logs

❌ **Still having issues if you see:**
- Consistent timeouts after 60+ seconds
- Empty responses
- Error messages in logs

## Need More Help?

If Nova Pro continues to timeout after these fixes:

1. **Check your specific region's capacity** - Some regions have better Nova Pro availability
2. **Try during off-peak hours** (early morning/late evening in your timezone)
3. **Contact AWS Support** if the issue persists for several hours

The key with Nova Pro is patience and proper request structuring. It's a powerful model but needs the right approach!