# Quick Fix: CDK Bootstrap Not Working

## 🚨 Run This First

**PowerShell:**
```powershell
.\diagnose.ps1
```

**CMD:**
```cmd
diagnose.bat
```

This will tell you exactly what's wrong!

---

## 🔧 Most Common Fixes (Try in Order)

### Fix 1: Configure AWS Credentials (90% of issues)

```bash
aws configure
```

Enter:
- **AWS Access Key ID**: Get from AWS Console → IAM → Users → Security Credentials
- **AWS Secret Access Key**: Get from AWS Console (shown only once when created)
- **Default region**: `us-east-1`
- **Default output format**: `json`

**Verify it worked:**
```bash
aws sts get-caller-identity
```

---

### Fix 2: Install Dependencies

```bash
npm install
```

**Verify it worked:**
```bash
dir node_modules\aws-cdk-lib
```

---

### Fix 3: Set Region

```bash
aws configure set region us-east-1
```

**Verify it worked:**
```bash
aws configure get region
```

---

### Fix 4: Navigate to Project Root

```bash
# Check current directory
cd

# Navigate to project (replace with your path)
cd C:\Users\Shreenath G\path\to\project

# Verify cdk.json exists
dir cdk.json
```

---

## ✅ Now Try Bootstrap Again

```bash
npx cdk bootstrap --verbose
```

---

## 🆘 Still Not Working?

### Get Your Account ID
```bash
aws sts get-caller-identity --query Account --output text
```

### Bootstrap with Explicit Account/Region
```bash
npx cdk bootstrap aws://YOUR-ACCOUNT-ID/us-east-1 --verbose
```

Replace `YOUR-ACCOUNT-ID` with the number from above.

---

## 📋 Complete Step-by-Step (If Nothing Else Works)

### Step 1: Verify Prerequisites
```bash
node --version
# Should show v18 or higher

npm --version
# Should show 9.x or higher

aws --version
# Should show aws-cli/2.x
```

### Step 2: Configure AWS
```bash
aws configure
```

### Step 3: Verify AWS Works
```bash
aws sts get-caller-identity
```

### Step 4: Navigate to Project
```bash
cd C:\Users\Shreenath G\your-project-folder
```

### Step 5: Verify Project Files
```bash
dir cdk.json
dir package.json
dir lib\ai-agent-stack.ts
```

### Step 6: Install Dependencies
```bash
npm install
```

### Step 7: Bootstrap
```bash
npx cdk bootstrap --verbose
```

---

## 🎯 What Should Happen

When bootstrap succeeds, you'll see:

```
 ⏳  Bootstrapping environment aws://123456789012/us-east-1...
Trusted accounts for deployment: (none)
Trusted accounts for lookup: (none)
Using default execution policy of 'arn:aws:iam::aws:policy/AdministratorAccess'.
CDKToolkit: creating CloudFormation changeset...
 ✅  Environment aws://123456789012/us-east-1 bootstrapped.
```

---

## 🔍 Common Error Messages

### "Need to perform AWS calls but no credentials found"
**Fix**: Run `aws configure`

### "Cannot find module 'aws-cdk-lib'"
**Fix**: Run `npm install`

### "Cannot find cdk.json"
**Fix**: Navigate to project root directory

### "User is not authorized to perform: cloudformation:CreateStack"
**Fix**: Add CloudFormation permissions to your IAM user in AWS Console

### "Region not specified"
**Fix**: Run `aws configure set region us-east-1`

---

## 💡 Pro Tips

1. **Always run commands from project root** (where cdk.json is)
2. **Use `--verbose` flag** to see detailed errors
3. **Check AWS Console** to verify your credentials work
4. **Restart terminal** after installing Node.js or AWS CLI

---

## 📞 Need More Help?

**Share this information:**
1. Output of `.\diagnose.ps1` or `diagnose.bat`
2. Full error message from `npx cdk bootstrap --verbose`
3. Output of `aws sts get-caller-identity`

**See detailed troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## ⚡ One-Line Fix (Try This)

```bash
aws configure && npm install && npx cdk bootstrap --verbose
```

This runs all three most common fixes in sequence!

---

**Good luck! 🚀**
