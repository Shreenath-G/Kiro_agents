# Fix Agent Configuration Issue

## 🚨 Problem

Your agent has `AgentCollaboration` set to `SUPERVISOR` mode, which requires collaborator agents. This is likely a default AWS setting.

**Agent ID**: `KKKWOGHCCZ`
**Error**: Cannot prepare agent without collaborators

---

## ✅ Solution: Delete and Redeploy

The fastest fix is to delete the current stack and redeploy with the correct configuration.

### Step 1: Delete the Current Stack

```powershell
# Delete the stack
npx cdk destroy

# Confirm by typing 'y' when prompted
```

Or manually delete in AWS Console:
1. Go to: https://console.aws.amazon.com/cloudformation/
2. Select `AdOptimizerAgentStack`
3. Click **Delete**
4. Confirm deletion

### Step 2: Update CDK Stack (Add Agent Configuration)

I'll update the stack to explicitly disable agent collaboration.

### Step 3: Redeploy

```powershell
npx cdk deploy
```

---

## 🔧 Alternative: Fix Existing Agent via AWS CLI

If you don't want to delete and redeploy, try updating the agent:

```powershell
# Update agent to disable collaboration
aws bedrock-agent update-agent `
  --agent-id KKKWOGHCCZ `
  --agent-name ad-optimizer-agent `
  --foundation-model amazon.nova-pro-v1:0 `
  --instruction "You are an expert digital advertising optimization agent..." `
  --agent-resource-role-arn (aws iam get-role --role-name AdOptimizerAgentStack-BedrockAgentRole* --query 'Role.Arn' --output text)

# Then try to prepare again
aws bedrock-agent prepare-agent --agent-id KKKWOGHCCZ
```

---

## 🎯 Recommended: Delete and Redeploy

This is the cleanest solution:

```powershell
# 1. Delete the stack
Write-Host "Deleting stack..." -ForegroundColor Yellow
npx cdk destroy

# 2. Wait for deletion to complete (5-10 minutes)
Write-Host "Waiting for deletion..." -ForegroundColor Yellow
do {
    $status = aws cloudformation describe-stacks --stack-name AdOptimizerAgentStack --query "Stacks[0].StackStatus" --output text 2>$null
    if ($status) {
        Write-Host "Status: $status"
        Start-Sleep -Seconds 30
    }
} while ($status)

Write-Host "✅ Stack deleted!" -ForegroundColor Green

# 3. Redeploy
Write-Host "Redeploying stack..." -ForegroundColor Yellow
npx cdk deploy

# 4. Get new Agent ID
$newAgentId = aws cloudformation describe-stacks --stack-name AdOptimizerAgentStack --query "Stacks[0].Outputs[?OutputKey=='AgentId'].OutputValue" --output text
Write-Host "New Agent ID: $newAgentId" -ForegroundColor Green

# 5. Prepare the agent
Write-Host "Preparing agent..." -ForegroundColor Yellow
aws bedrock-agent prepare-agent --agent-id $newAgentId

# 6. Wait for preparation
Start-Sleep -Seconds 60
$status = aws bedrock-agent get-agent --agent-id $newAgentId --query "agent.agentStatus" --output text
Write-Host "Agent Status: $status" -ForegroundColor Cyan
```

---

## 📋 Quick Commands

### Delete Stack
```powershell
npx cdk destroy
```

### Check Deletion Status
```powershell
aws cloudformation describe-stacks --stack-name AdOptimizerAgentStack --query "Stacks[0].StackStatus"
```

### Redeploy
```powershell
npx cdk deploy
```

---

## ⏱️ Timeline

- **Delete**: 5-10 minutes
- **Redeploy**: 10-15 minutes
- **Total**: ~20 minutes

---

## 🎯 What I'll Do

Let me update the CDK stack to explicitly set the agent configuration to avoid this issue.
