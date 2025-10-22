# Nova Pro Lambda Timeout Fix

## Root Cause Analysis

The issue is **NOT with Nova Pro itself** - it's with Lambda function invocation timeouts. Here's what's happening:

1. ✅ Nova Pro responds to simple text requests (like "Hello")
2. ❌ Nova Pro times out when trying to invoke Lambda functions (like "Get campaigns")

This indicates the problem is in the **Lambda function invocation chain**, not the model.

## The Real Problem

When Nova Pro tries to call your Lambda functions through Bedrock Agent action groups, one of these is happening:

1. **Lambda Cold Start**: Functions take 10-15 seconds to initialize
2. **IAM Permission Issues**: Bedrock can't invoke the Lambda functions
3. **Lambda Function Errors**: Functions are failing internally
4. **Network/VPC Issues**: Lambda functions can't reach AWS services

## Immediate Fixes

### Fix 1: Increase Lambda Memory (Reduces Cold Start)

```typescript
// In lib/ai-agent-stack.ts, increase memory for all Lambda functions:

// Google Ads Function
const googleAdsFunction = new lambda.Function(this, 'GoogleAdsFunction', {
  runtime: lambda.Runtime.PYTHON_3_12,
  handler: 'index.handler',
  code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/google-ads')),
  timeout: cdk.Duration.seconds(120), // Increased from 60
  memorySize: 1024, // Increased from 512
  environment: {
    BUCKET_NAME: campaignDataBucket.bucketName,
    METRICS_TABLE: metricsTable.tableName,
    SECRETS_ARN: apiKeysSecret.secretArn,
  },
});

// Meta Ads Function  
const metaAdsFunction = new lambda.Function(this, 'MetaAdsFunction', {
  runtime: lambda.Runtime.PYTHON_3_12,
  handler: 'index.handler',
  code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/meta-ads')),
  timeout: cdk.Duration.seconds(120), // Increased from 60
  memorySize: 1024, // Increased from 512
  environment: {
    BUCKET_NAME: campaignDataBucket.bucketName,
    METRICS_TABLE: metricsTable.tableName,
    SECRETS_ARN: apiKeysSecret.secretArn,
  },
});

// Budget Optimizer Function
const budgetOptimizerFunction = new lambda.Function(this, 'BudgetOptimizerFunction', {
  runtime: lambda.Runtime.PYTHON_3_12,
  handler: 'index.handler',
  code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/budget-optimizer')),
  timeout: cdk.Duration.seconds(120), // Increased from 60
  memorySize: 1024, // Increased from 512
  environment: {
    BUCKET_NAME: campaignDataBucket.bucketName,
    METRICS_TABLE: metricsTable.tableName,
  },
});
```

### Fix 2: Add Lambda Warming (Prevents Cold Starts)

Add this to your CDK stack:

```typescript
// Add EventBridge rule to warm Lambda functions every 5 minutes
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';

// Warm Google Ads function
new events.Rule(this, 'WarmGoogleAdsFunction', {
  schedule: events.Schedule.rate(cdk.Duration.minutes(5)),
  targets: [new targets.LambdaFunction(googleAdsFunction, {
    event: events.RuleTargetInput.fromObject({
      source: 'warming',
      apiPath: '/health',
      httpMethod: 'GET'
    })
  })]
});

// Warm Meta Ads function
new events.Rule(this, 'WarmMetaAdsFunction', {
  schedule: events.Schedule.rate(cdk.Duration.minutes(5)),
  targets: [new targets.LambdaFunction(metaAdsFunction, {
    event: events.RuleTargetInput.fromObject({
      source: 'warming',
      apiPath: '/health', 
      httpMethod: 'GET'
    })
  })]
});
```

### Fix 3: Add Health Check Endpoints

Add this to each Lambda function (e.g., `lambda/google-ads/index.py`):

```python
def handler(event, context):
    """
    Google Ads integration tool for the AI agent.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Handle warming requests
    if event.get('source') == 'warming':
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'warm', 'timestamp': datetime.now().isoformat()})
        }
    
    # Handle health checks
    if event.get('apiPath') == '/health':
        return success_response(event, {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'function': 'google-ads'
        })
    
    # ... rest of your existing code
```

## Quick Implementation

Run these commands to apply the fixes:

```bash
# 1. The CDK stack has already been updated with increased timeouts
# 2. Deploy the changes
npx cdk deploy

# 3. Test after deployment
python test-nova-pro.py
```

## Alternative: Test Lambda Functions Directly

Before testing with Nova Pro, verify Lambda functions work:

```bash
# Test Google Ads function directly
aws lambda invoke \
  --function-name AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of \
  --payload '{"apiPath":"/campaigns","httpMethod":"GET","parameters":[]}' \
  --cli-binary-format raw-in-base64-out \
  lambda-test.json

cat lambda-test.json
```

## Root Cause Verification

### Check Lambda Function Status
```bash
# Check if functions are ready
aws lambda get-function --function-name AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of

# Check recent invocations
aws lambda get-function-configuration --function-name AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of
```

### Check IAM Permissions
```bash
# Verify Bedrock can invoke Lambda
aws iam get-role --role-name AdOptimizerAgentStack-BedrockAgentRole*

# Check Lambda resource policy
aws lambda get-policy --function-name AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of
```

## Expected Results After Fix

✅ **Success indicators:**
- Lambda functions respond within 2-5 seconds
- Nova Pro successfully calls "Get Google Ads campaigns"
- No more "dependency timeout" errors
- Consistent performance across requests

❌ **If still failing:**
- Check CloudWatch logs for Lambda errors
- Verify DynamoDB table exists and is accessible
- Check S3 bucket permissions
- Verify Secrets Manager access

## Monitoring the Fix

```bash
# Watch Lambda logs in real-time
aws logs tail /aws/lambda/AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of --follow

# Check Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=AdOptimizerAgentStack-GoogleAdsFunctionA96CDAD3-R6fAb6sPH1Of \
  --start-time 2025-01-22T10:00:00Z \
  --end-time 2025-01-22T11:00:00Z \
  --period 300 \
  --statistics Average,Maximum
```

## The Bottom Line

**Nova Pro is working fine** - the timeout is happening in the Lambda function invocation layer. The fixes above address:

1. **Cold starts** (increased memory + warming)
2. **Timeout limits** (increased from 60s to 120s) 
3. **Function readiness** (health checks)

After applying these fixes, Nova Pro should work reliably with your Lambda functions.