# Troubleshooting Guide: CDK Bootstrap Issues

## Problem: `npx cdk bootstrap` Not Working

### Common Issues and Solutions

---

## Issue 1: AWS Credentials Not Configured

### Symptoms:
```
Error: Need to perform AWS calls for account XXX, but no credentials found
```

### Solution:

**Step 1: Configure AWS CLI**
```bash
aws configure
```

You'll be prompted for:
```
AWS Access Key ID [None]: YOUR_ACCESS_KEY
AWS Secret Access Key [None]: YOUR_SECRET_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

**Step 2: Verify Configuration**
```bash
aws sts get-caller-identity
```

Should return:
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

**Step 3: Try Bootstrap Again**
```bash
npx cdk bootstrap
```

---

## Issue 2: Node Modules Not Installed

### Symptoms:
```
Error: Cannot find module 'aws-cdk-lib'
```

### Solution:

**Step 1: Install Dependencies**
```bash
npm install
```

**Step 2: Verify Installation**
```bash
npm list aws-cdk-lib
```

Should show:
```
aws-ai-ad-optimizer@1.0.0
└── aws-cdk-lib@2.170.0
```

**Step 3: Try Bootstrap Again**
```bash
npx cdk bootstrap
```

---

## Issue 3: Wrong Directory

### Symptoms:
```
Error: Cannot find cdk.json
```

### Solution:

**Step 1: Check Current Directory**
```bash
# Windows (CMD)
cd

# Windows (PowerShell)
pwd

# Should show: C:\Users\...\your-project-folder
```

**Step 2: Navigate to Project Root**
```bash
cd C:\Users\Shreenath G\path\to\your\project
```

**Step 3: Verify cdk.json Exists**
```bash
# Windows (CMD)
dir cdk.json

# Windows (PowerShell)
ls cdk.json
```

**Step 4: Try Bootstrap Again**
```bash
npx cdk bootstrap
```

---

## Issue 4: Insufficient AWS Permissions

### Symptoms:
```
Error: User: arn:aws:iam::XXX:user/YYY is not authorized to perform: cloudformation:CreateStack
```

### Solution:

Your AWS user needs these permissions:
- CloudFormation (create/update stacks)
- S3 (create buckets)
- IAM (create roles)
- SSM (parameter store)

**Option A: Use Administrator Access (Easiest for Testing)**
1. Go to AWS Console → IAM → Users
2. Select your user
3. Add permission: `AdministratorAccess` (managed policy)

**Option B: Use Specific Permissions**
Attach these policies:
- `AWSCloudFormationFullAccess`
- `IAMFullAccess`
- `AmazonS3FullAccess`

**Step 3: Try Bootstrap Again**
```bash
npx cdk bootstrap
```

---

## Issue 5: Region Not Specified

### Symptoms:
```
Error: Region not specified
```

### Solution:

**Option A: Set Default Region in AWS Config**
```bash
aws configure set region us-east-1
```

**Option B: Specify Region in Bootstrap Command**
```bash
npx cdk bootstrap aws://ACCOUNT-NUMBER/us-east-1
```

Replace `ACCOUNT-NUMBER` with your AWS account ID (get it from `aws sts get-caller-identity`)

**Option C: Set Environment Variable**
```bash
# Windows (CMD)
set AWS_DEFAULT_REGION=us-east-1

# Windows (PowerShell)
$env:AWS_DEFAULT_REGION="us-east-1"
```

---

## Issue 6: CDK Not Installed Globally

### Symptoms:
```
'cdk' is not recognized as an internal or external command
```

### Solution:

**Use npx (Recommended)**
```bash
npx cdk bootstrap
```

**Or Install CDK Globally**
```bash
npm install -g aws-cdk
cdk bootstrap
```

---

## Issue 7: Network/Firewall Issues

### Symptoms:
```
Error: connect ETIMEDOUT
Error: getaddrinfo ENOTFOUND
```

### Solution:

**Step 1: Check Internet Connection**
```bash
ping aws.amazon.com
```

**Step 2: Check Proxy Settings (if behind corporate firewall)**
```bash
# Windows (CMD)
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080

# Windows (PowerShell)
$env:HTTP_PROXY="http://proxy.company.com:8080"
$env:HTTPS_PROXY="http://proxy.company.com:8080"
```

**Step 3: Try Bootstrap Again**
```bash
npx cdk bootstrap
```

---

## Issue 8: TypeScript Compilation Errors

### Symptoms:
```
Error: Compilation failed
```

### Solution:

**Step 1: Check TypeScript Installation**
```bash
npm list typescript
```

**Step 2: Compile Manually**
```bash
npm run build
```

**Step 3: Fix Any Errors**
Look at the error messages and fix TypeScript issues in:
- `lib/ai-agent-stack.ts`
- `bin/app.ts`

**Step 4: Try Bootstrap Again**
```bash
npx cdk bootstrap
```

---

## Complete Troubleshooting Workflow

### Step-by-Step Diagnostic

**1. Verify Prerequisites**
```bash
# Check Node.js
node --version
# Should be v18 or higher

# Check npm
npm --version

# Check AWS CLI
aws --version
# Should be v2.x
```

**2. Verify AWS Credentials**
```bash
aws sts get-caller-identity
```

**3. Verify Project Setup**
```bash
# Check you're in the right directory
dir cdk.json

# Check dependencies are installed
dir node_modules
```

**4. Install Dependencies (if needed)**
```bash
npm install
```

**5. Try Bootstrap with Verbose Output**
```bash
npx cdk bootstrap --verbose
```

This will show detailed error messages.

---

## Alternative: Manual Bootstrap

If automatic bootstrap fails, you can bootstrap manually:

**Step 1: Get Your Account ID**
```bash
aws sts get-caller-identity --query Account --output text
```

**Step 2: Bootstrap with Explicit Parameters**
```bash
npx cdk bootstrap aws://YOUR-ACCOUNT-ID/us-east-1 --verbose
```

Replace `YOUR-ACCOUNT-ID` with the number from step 1.

---

## Still Not Working?

### Collect Diagnostic Information

**1. Check CDK Version**
```bash
npx cdk --version
```

**2. Check AWS CLI Configuration**
```bash
aws configure list
```

**3. Check Environment Variables**
```bash
# Windows (CMD)
set | findstr AWS

# Windows (PowerShell)
Get-ChildItem Env: | Where-Object {$_.Name -like "*AWS*"}
```

**4. Run Bootstrap with Debug**
```bash
npx cdk bootstrap --verbose --debug
```

**5. Share the Error**
Copy the full error message and we can diagnose further.

---

## Quick Fix Commands (Try These in Order)

```bash
# 1. Verify AWS credentials
aws sts get-caller-identity

# 2. Set region
aws configure set region us-east-1

# 3. Navigate to project directory
cd C:\Users\Shreenath G\path\to\project

# 4. Install dependencies
npm install

# 5. Bootstrap with verbose output
npx cdk bootstrap --verbose

# 6. If that fails, try with explicit account/region
npx cdk bootstrap aws://$(aws sts get-caller-identity --query Account --output text)/us-east-1
```

---

## Common Error Messages and Solutions

### Error: "Cannot find module 'aws-cdk-lib'"
**Solution**: Run `npm install`

### Error: "Need to perform AWS calls but no credentials found"
**Solution**: Run `aws configure`

### Error: "User is not authorized to perform: cloudformation:CreateStack"
**Solution**: Add CloudFormation permissions to your IAM user

### Error: "Cannot find cdk.json"
**Solution**: Navigate to project root directory

### Error: "Region not specified"
**Solution**: Run `aws configure set region us-east-1`

### Error: "EACCES: permission denied"
**Solution**: Run as administrator or fix npm permissions

### Error: "Compilation failed"
**Solution**: Run `npm run build` and fix TypeScript errors

---

## Windows-Specific Issues

### PowerShell Execution Policy

If you get execution policy errors:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Path Issues

If commands aren't found:

```bash
# Add Node.js to PATH
setx PATH "%PATH%;C:\Program Files\nodejs"

# Restart terminal after this
```

---

## What Should Happen When Bootstrap Succeeds

You should see output like:

```
 ⏳  Bootstrapping environment aws://123456789012/us-east-1...
Trusted accounts for deployment: (none)
Trusted accounts for lookup: (none)
Using default execution policy of 'arn:aws:iam::aws:policy/AdministratorAccess'. Pass '--cloudformation-execution-policies' to customize.
CDKToolkit: creating CloudFormation changeset...
 ✅  Environment aws://123456789012/us-east-1 bootstrapped.
```

This creates:
- CloudFormation stack: `CDKToolkit`
- S3 bucket: `cdk-hnb659fds-assets-123456789012-us-east-1`
- IAM roles for CDK

---

## Next Steps After Successful Bootstrap

```bash
# 1. Synthesize the stack (optional, to check for errors)
npx cdk synth

# 2. Deploy the stack
npx cdk deploy

# 3. Follow the prompts
# Type 'y' when asked to approve changes
```

---

## Need More Help?

**Provide this information:**
1. Full error message
2. Output of `aws sts get-caller-identity`
3. Output of `node --version`
4. Output of `npm --version`
5. Output of `aws --version`
6. Your operating system (Windows version)
7. Output of `npx cdk bootstrap --verbose`

---

## Contact & Resources

- **AWS CDK Documentation**: https://docs.aws.amazon.com/cdk/
- **AWS CDK GitHub**: https://github.com/aws/aws-cdk
- **AWS Support**: https://console.aws.amazon.com/support/

---

**Most Common Solution**: 90% of bootstrap issues are fixed by:
1. Running `aws configure` to set up credentials
2. Running `npm install` to install dependencies
3. Being in the correct project directory

Try those three things first! 🚀
