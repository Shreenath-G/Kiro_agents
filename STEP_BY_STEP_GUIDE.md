# Complete Step-by-Step Deployment & Working Guide

## 🎯 Overview

This guide walks you through **every single step** from zero to a fully working AI Advertisement Optimization Agent.

**Total Time**: 30-45 minutes
**Difficulty**: Beginner-friendly
**Cost**: ~$25/month after deployment

---

## 📋 Table of Contents

1. [Prerequisites Setup](#1-prerequisites-setup)
2. [AWS Account Configuration](#2-aws-account-configuration)
3. [Project Setup](#3-project-setup)
4. [Deployment](#4-deployment)
5. [Agent Configuration](#5-agent-configuration)
6. [Testing](#6-testing)
7. [Understanding How It Works](#7-understanding-how-it-works)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites Setup

### Step 1.1: Install Node.js

**Windows:**
1. Go to https://nodejs.org/
2. Download "LTS" version (18.x or higher)
3. Run installer
4. Click "Next" through all prompts
5. Verify installation:
```cmd
node --version
npm --version
```
Expected output: `v18.x.x` or higher

**Mac:**
```bash
brew install node@18
node --version
npm --version
```

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
npm --version
```

### Step 1.2: Install Python

**Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.9 or higher
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify:
```cmd
python --version
```
Expected: `Python 3.9.x` or higher

**Mac:**
```bash
brew install python@3.9
python3 --version
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.9 python3-pip
python3 --version
```

### Step 1.3: Install AWS CLI

**Windows:**
1. Download: https://awscli.amazonaws.com/AWSCLIV2.msi
2. Run installer
3. Verify:
```cmd
aws --version
```

**Mac:**
```bash
brew install awscli
aws --version
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### Step 1.4: Install Git (Optional but Recommended)

**Windows:**
- Download from https://git-scm.com/download/win
- Run installer with default settings

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

---

## 2. AWS Account Configuration

### Step 2.1: Create AWS Account

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the signup process
4. **You'll need**:
   - Email address
   - Credit card (for billing)
   - Phone number (for verification)

**Note**: AWS Free Tier covers some services, but Bedrock has separate pricing.

### Step 2.2: Create IAM User

1. Log into AWS Console: https://console.aws.amazon.com/
2. Search for "IAM" in the top search bar
3. Click "Users" in left sidebar
4. Click "Create user"
5. Enter username: `kiro-agent-deployer`
6. Click "Next"
7. Select "Attach policies directly"
8. Search and select these policies:
   - `AdministratorAccess` (for initial setup)
   - Or create custom policy with these permissions:
     - CloudFormation full access
     - Lambda full access
     - S3 full access
     - DynamoDB full access
     - Bedrock full access
     - IAM role creation
     - Secrets Manager full access
9. Click "Next" → "Create user"

### Step 2.3: Create Access Keys

1. Click on the user you just created
2. Go to "Security credentials" tab
3. Scroll to "Access keys"
4. Click "Create access key"
5. Select "Command Line Interface (CLI)"
6. Check the confirmation box
7. Click "Next" → "Create access key"
8. **IMPORTANT**: Copy both:
   - Access key ID
   - Secret access key
9. Click "Download .csv file" (backup)

### Step 2.4: Configure AWS CLI

Open terminal/command prompt:

```bash
aws configure
```

Enter when prompted:
```
AWS Access Key ID: [paste your access key]
AWS Secret Access Key: [paste your secret key]
Default region name: us-east-1
Default output format: json
```

Verify configuration:
```bash
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDAXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/kiro-agent-deployer"
}
```

### Step 2.5: Enable Amazon Bedrock Access

1. Go to AWS Console
2. Search for "Bedrock" in top search bar
3. Click "Amazon Bedrock"
4. In left sidebar, click "Model access"
5. Click "Manage model access" (orange button)
6. Find "Amazon" section
7. Check the box for "Nova Pro"
8. Scroll down and click "Request model access"
9. Wait 1-2 minutes for approval
10. Refresh page - status should show "Access granted" ✅

**Important**: If you don't see Nova Pro, your region might not support it yet. Try:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)

---

## 3. Project Setup

### Step 3.1: Download Project Files

**Option A: Using Git**
```bash
git clone https://github.com/your-repo/kiro-agents.git
cd kiro-agents
```

**Option B: Download ZIP**
1. Download project ZIP file
2. Extract to a folder
3. Open terminal in that folder

### Step 3.2: Verify Project Structure

Run this command to see all files:

**Windows:**
```cmd
dir /s /b
```

**Mac/Linux:**
```bash
find . -type f
```

You should see:
```
./package.json
./tsconfig.json
./cdk.json
./bin/app.ts
./lib/ai-agent-stack.ts
./lambda/google-ads/index.py
./lambda/meta-ads/index.py
./lambda/analytics/index.py
./lambda/budget-optimizer/index.py
./lambda/storage/index.py
./test-agent.py
./interactive-demo.py
... and more
```

### Step 3.3: Install Node.js Dependencies

```bash
npm install
```

This will:
- Download all required packages
- Create `node_modules/` folder
- Take 2-3 minutes

Expected output:
```
added 500+ packages in 2m
```

### Step 3.4: Verify Installation

```bash
npx cdk --version
```

Expected output:
```
2.170.0 (build xxxxxx)
```

---

## 4. Deployment

### Step 4.1: Bootstrap CDK (First Time Only)

This creates necessary AWS resources for CDK:

```bash
npx cdk bootstrap
```

**What this does**:
- Creates S3 bucket for CDK assets
- Creates IAM roles for deployments
- Sets up CloudFormation stack

Expected output:
```
 ✅  Environment aws://123456789012/us-east-1 bootstrapped
```

**Time**: 2-3 minutes

### Step 4.2: Review What Will Be Created

```bash
npx cdk synth
```

This shows the CloudFormation template. You'll see:
- Lambda functions (5)
- S3 bucket
- DynamoDB table
- Bedrock Agent
- IAM roles
- Secrets Manager secret

### Step 4.3: Deploy the Stack

```bash
npx cdk deploy
```

**What happens**:
1. CDK synthesizes CloudFormation template
2. Uploads Lambda code to S3
3. Creates all AWS resources
4. Configures Bedrock Agent

You'll see:
```
Do you wish to deploy these changes (y/n)? 
```

Type `y` and press Enter.

**Deployment Progress**:
```
AdOptimizerAgentStack: deploying...
[0%] start: Publishing asset...
[25%] success: Published asset...
[50%] start: Publishing Lambda functions...
[75%] success: Published Lambda functions...
[100%] success: Deployed AdOptimizerAgentStack

Outputs:
AdOptimizerAgentStack.AgentId = ABCDEFGHIJ
AdOptimizerAgentStack.CampaignDataBucketName = ad-optimizer-data-123456789012
AdOptimizerAgentStack.MetricsTableName = ad-optimizer-metrics
AdOptimizerAgentStack.APIKeysSecretArn = arn:aws:secretsmanager:...

Stack ARN:
arn:aws:cloudformation:us-east-1:123456789012:stack/AdOptimizerAgentStack/...
```

**IMPORTANT**: Copy the `AgentId` - you'll need it!

**Time**: 5-10 minutes

### Step 4.4: Verify Deployment

Check if resources were created:

```bash
# Check Lambda functions
aws lambda list-functions --query 'Functions[?contains(FunctionName, `AdOptimizer`)].FunctionName'

# Check S3 bucket
aws s3 ls | grep ad-optimizer

# Check DynamoDB table
aws dynamodb list-tables --query 'TableNames[?contains(@, `ad-optimizer`)]'

# Check Bedrock Agent
aws bedrock-agent list-agents --region us-east-1
```

---

## 5. Agent Configuration

### Step 5.1: Find Your Agent in AWS Console

1. Go to AWS Console: https://console.aws.amazon.com/
2. Search for "Bedrock" in top search bar
3. Click "Amazon Bedrock"
4. In left sidebar, click "Agents"
5. You should see: `ad-optimizer-agent`

### Step 5.2: Create Agent Alias

1. Click on `ad-optimizer-agent`
2. Click "Create alias" button (top right)
3. Enter alias name: `production`
4. Select version: `1` (or latest)
5. Click "Create alias"

**Wait 1-2 minutes** for alias to be ready.

### Step 5.3: Get Agent Details

On the agent page, note these values:
- **Agent ID**: `ABCDEFGHIJ` (10 characters)
- **Alias ID**: `TSTALIASID` or custom ID

**Save these** - you'll need them for testing!

### Step 5.4: Test in AWS Console (Optional)

1. Stay on the agent page
2. Click "Test" tab at the top
3. In the chat box, type:
```
Show me all my campaigns
```
4. Press Enter
5. You should see the agent respond with campaign data

If this works, your agent is ready! ✅

---

## 6. Testing

### Step 6.1: Run Automated Tests

Open terminal in project folder:

```bash
python test-agent.py
```

When prompted:
```
Enter your Agent ID: [paste your Agent ID]
Enter your Agent Alias ID: [press Enter for TSTALIASID or paste your alias]
```

**What happens**:
The script runs 6 automated tests:
1. Get campaign overview
2. Analyze specific campaign
3. Budget optimization
4. Autonomous multi-step optimization
5. Cross-platform analysis
6. Creative testing

**Expected output**:
```
🤖 AI Advertisement Optimization Agent - Test Client
======================================================================

📋 Test 1: Get Campaign Overview
======================================================================
USER: Show me all my Google Ads and Meta Ads campaigns with their current performance.
======================================================================

🤖 Agent is thinking...

I've analyzed your campaigns across Google Ads and Meta Ads:

📊 Google Ads Campaigns:
1. Search - Brand Keywords (goog-camp-001)
   Budget: $1,500 | ROAS: 6.21x | Status: ✅ Excellent
...

✅ All tests completed!
```

**Time**: 3-5 minutes for all tests

### Step 6.2: Run Interactive Demo

```bash
python interactive-demo.py
```

When prompted, enter your Agent ID and Alias ID.

**Try these prompts**:

1. **Campaign Overview**:
```
Show me all my campaigns and their performance
```

2. **Performance Analysis**:
```
Analyze campaign goog-camp-001 and identify any issues
```

3. **Budget Optimization**:
```
I have $5000 monthly budget. Optimize allocation across all campaigns to maximize ROAS
```

4. **Autonomous Optimization**:
```
Find my worst performing campaign and take action to improve it. Reduce its budget and reallocate to better performers.
```

5. **Cross-Platform Analysis**:
```
Compare Google Ads vs Meta Ads. Which platform gives better ROI?
```

6. **Ad Fatigue Detection**:
```
Are any of my campaigns showing signs of ad fatigue? What should I do?
```

**To exit**: Type `quit` or press Ctrl+C

---

## 7. Understanding How It Works

### Step 7.1: What Just Happened?

When you sent a prompt, here's what occurred:

```
1. Your prompt → Bedrock Agent (Nova Pro)
2. Agent reasons about the task
3. Agent decides which tools to use
4. Agent calls Lambda functions:
   - google_ads.get_campaigns()
   - meta_ads.get_campaigns()
   - analytics.analyze_performance()
   - budget_optimizer.optimize()
5. Lambda functions query DynamoDB for metrics
6. Lambda functions return data to agent
7. Agent synthesizes information
8. Agent responds to you
```

### Step 7.2: Check What's Stored

**View DynamoDB Data**:
```bash
aws dynamodb scan --table-name ad-optimizer-metrics --limit 5
```

**View S3 Data**:
```bash
aws s3 ls s3://ad-optimizer-data-YOUR-ACCOUNT-ID/insights/
```

### Step 7.3: View Lambda Logs

```bash
# Google Ads function logs
aws logs tail /aws/lambda/AdOptimizerAgentStack-GoogleAdsFunction --follow

# Analytics function logs
aws logs tail /aws/lambda/AdOptimizerAgentStack-AnalyticsFunction --follow
```

Press Ctrl+C to stop following logs.

### Step 7.4: Understanding the Agent's Reasoning

The agent uses Nova Pro's reasoning to:

**Example Decision Process**:
```
User: "Optimize my campaigns"

Agent's Internal Reasoning:
1. "I need to see all campaigns first"
   → Calls google_ads.get_campaigns()
   → Calls meta_ads.get_campaigns()

2. "Now I have 6 campaigns. Let me analyze each"
   → Calls analytics.analyze_performance() 6 times

3. "Campaign goog-camp-002 has 0.85x ROAS - losing money"
   → This is a problem

4. "Campaign goog-camp-001 has 6.21x ROAS - very profitable"
   → Should allocate more here

5. "Let me calculate optimal allocation"
   → Calls budget_optimizer.optimize()

6. "Makes sense. Execute the changes"
   → Calls google_ads.update_budget()

7. "Document this decision"
   → Calls storage.store()

8. "Explain to user what I did"
   → Synthesizes response
```

This is **autonomous reasoning**, not rule-based automation!

---

## 8. Troubleshooting

### Issue 1: "Model not found" or "Access denied"

**Solution**:
1. Go to AWS Console → Bedrock → Model access
2. Verify Nova Pro shows "Access granted"
3. If not, request access again
4. Wait 5 minutes and try again

### Issue 2: "Agent not found"

**Solution**:
1. Wait 2-3 minutes after deployment
2. Verify agent exists:
```bash
aws bedrock-agent list-agents --region us-east-1
```
3. Check you're using correct Agent ID

### Issue 3: "Permission denied" errors

**Solution**:
1. Check IAM user has correct permissions
2. Verify AWS CLI is configured:
```bash
aws sts get-caller-identity
```
3. Re-run `aws configure` if needed

### Issue 4: Lambda timeout errors

**Solution**:
1. Increase timeout in `lib/ai-agent-stack.ts`:
```typescript
timeout: cdk.Duration.seconds(90),  // Increase from 60
```
2. Redeploy:
```bash
npx cdk deploy
```

### Issue 5: "No module named 'boto3'"

**Solution**:
Lambda includes boto3 by default. If error persists:
1. Check Lambda runtime is Python 3.12
2. Verify in AWS Console → Lambda → Functions

### Issue 6: DynamoDB "Item not found"

**Solution**:
This is normal on first run. The agent will create data as it runs.

### Issue 7: Cost concerns

**Check current costs**:
```bash
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

**Expected costs**:
- Bedrock: ~$10-15/month
- Lambda: ~$2-3/month
- DynamoDB: ~$3-5/month
- S3: ~$1-2/month
- **Total**: ~$20-25/month

---

## 9. Next Steps

### Step 9.1: Add Real API Keys (Optional)

To connect to real Google Ads and Meta Ads:

```bash
aws secretsmanager update-secret \
  --secret-id ad-optimizer/api-keys \
  --secret-string '{
    "googleAdsClientId": "YOUR_CLIENT_ID",
    "googleAdsClientSecret": "YOUR_CLIENT_SECRET",
    "googleAdsRefreshToken": "YOUR_REFRESH_TOKEN",
    "googleAdsDeveloperToken": "YOUR_DEVELOPER_TOKEN",
    "metaAccessToken": "YOUR_META_ACCESS_TOKEN",
    "metaAdAccountId": "YOUR_AD_ACCOUNT_ID"
  }'
```

### Step 9.2: Schedule Continuous Optimization

Add EventBridge rule to run agent hourly:

```typescript
// Add to lib/ai-agent-stack.ts
const rule = new events.Rule(this, 'HourlyOptimization', {
  schedule: events.Schedule.rate(cdk.Duration.hours(1)),
});

rule.addTarget(new targets.LambdaFunction(analyticsFunction));
```

Redeploy:
```bash
npx cdk deploy
```

### Step 9.3: Set Up Monitoring

Create CloudWatch dashboard:
1. Go to CloudWatch in AWS Console
2. Click "Dashboards" → "Create dashboard"
3. Add widgets for:
   - Lambda invocations
   - DynamoDB read/write units
   - Bedrock API calls
   - Error rates

### Step 9.4: Clean Up (When Done Testing)

To remove everything and stop charges:

```bash
npx cdk destroy
```

Type `y` to confirm.

This will delete:
- All Lambda functions
- DynamoDB table
- S3 bucket (and contents)
- Bedrock Agent
- All IAM roles

**Time**: 2-3 minutes

---

## 10. Quick Reference

### Common Commands

```bash
# Deploy
npx cdk deploy

# Check deployment status
aws cloudformation describe-stacks --stack-name AdOptimizerAgentStack

# View Lambda functions
aws lambda list-functions | grep AdOptimizer

# View logs
aws logs tail /aws/lambda/AdOptimizerAgentStack-GoogleAdsFunction --follow

# Test agent
python test-agent.py

# Interactive demo
python interactive-demo.py

# Destroy everything
npx cdk destroy
```

### Important URLs

- AWS Console: https://console.aws.amazon.com/
- Bedrock Console: https://console.aws.amazon.com/bedrock/
- Lambda Console: https://console.aws.amazon.com/lambda/
- DynamoDB Console: https://console.aws.amazon.com/dynamodb/
- S3 Console: https://console.aws.amazon.com/s3/

### Support

- Check CloudWatch logs for errors
- Review DEPLOYMENT.md for detailed troubleshooting
- Check VERIFICATION_CHECKLIST.md for validation steps

---

## ✅ Success Checklist

- [ ] Node.js installed and verified
- [ ] Python installed and verified
- [ ] AWS CLI installed and configured
- [ ] AWS account created
- [ ] IAM user created with access keys
- [ ] Bedrock Nova Pro access granted
- [ ] Project files downloaded
- [ ] npm install completed
- [ ] CDK bootstrapped
- [ ] Stack deployed successfully
- [ ] Agent ID and Alias ID obtained
- [ ] Agent tested in AWS Console
- [ ] Automated tests passed
- [ ] Interactive demo works
- [ ] Understanding how it works

**If all checked, you're done! 🎉**

---

**Congratulations! Your AI Advertisement Optimization Agent is now live and working!** 🚀
