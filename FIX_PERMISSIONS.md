# Fix IAM Permissions for CDK Bootstrap

## 🎯 Your Issue

**User**: `arn:aws:iam::793323451177:user/kiro-agent-deployer`
**Error**: Not authorized to perform `cloudformation:DescribeStacks`

Your IAM user needs CloudFormation permissions to bootstrap CDK.

---

## ✅ Solution: Add Required Permissions

You have **3 options** (from easiest to most secure):

---

## Option 1: Add Administrator Access (Easiest - For Testing)

### Step 1: Go to AWS Console
1. Open https://console.aws.amazon.com/iam/
2. Sign in with your root account or an admin user

### Step 2: Navigate to Your User
1. Click **Users** in the left sidebar
2. Click on **kiro-agent-deployer**

### Step 3: Add Administrator Policy
1. Click the **Permissions** tab
2. Click **Add permissions** → **Attach policies directly**
3. Search for: `AdministratorAccess`
4. Check the box next to **AdministratorAccess**
5. Click **Add permissions**

### Step 4: Try Bootstrap Again
```bash
npx cdk bootstrap
```

**✅ This should work now!**

---

## Option 2: Add Specific CDK Permissions (Recommended)

If you don't want full admin access, add these specific policies:

### Step 1: Go to AWS Console
1. Open https://console.aws.amazon.com/iam/
2. Click **Users** → **kiro-agent-deployer**

### Step 2: Attach These Policies
Click **Add permissions** → **Attach policies directly**, then add:

1. ✅ **AWSCloudFormationFullAccess**
2. ✅ **IAMFullAccess**
3. ✅ **AmazonS3FullAccess**
4. ✅ **AWSLambda_FullAccess**
5. ✅ **AmazonDynamoDBFullAccess**
6. ✅ **SecretsManagerReadWrite**

### Step 3: Try Bootstrap Again
```bash
npx cdk bootstrap
```

---

## Option 3: Create Custom Policy (Most Secure)

### Step 1: Create Custom Policy

1. Go to IAM Console → **Policies** → **Create policy**
2. Click **JSON** tab
3. Paste this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "iam:*",
        "ssm:*",
        "ecr:*"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Click **Next**
5. Name it: `CDKBootstrapPolicy`
6. Click **Create policy**

### Step 2: Attach to User

1. Go to **Users** → **kiro-agent-deployer**
2. Click **Add permissions** → **Attach policies directly**
3. Search for: `CDKBootstrapPolicy`
4. Check the box
5. Click **Add permissions**

### Step 3: Try Bootstrap Again
```bash
npx cdk bootstrap
```

---

## Option 4: Use a Different User (Alternative)

If you can't modify `kiro-agent-deployer`, use a different AWS user:

### Step 1: Configure Different Credentials
```bash
aws configure --profile admin
```

Enter credentials for a user with admin access.

### Step 2: Bootstrap with Profile
```bash
npx cdk bootstrap --profile admin
```

### Step 3: Deploy with Profile
```bash
npx cdk deploy --profile admin
```

---

## 🔍 Verify Permissions Were Added

After adding permissions, verify:

```bash
# This should now work
aws cloudformation describe-stacks --stack-name CDKToolkit

# If it returns "Stack not found" - that's OK, it means permissions work
# If it returns "AccessDenied" - permissions not added yet
```

---

## 📋 Minimum Required Permissions for CDK

For CDK bootstrap, your user needs:

### CloudFormation
- `cloudformation:CreateStack`
- `cloudformation:DescribeStacks`
- `cloudformation:DescribeStackEvents`
- `cloudformation:GetTemplate`
- `cloudformation:UpdateStack`
- `cloudformation:DeleteStack`

### S3
- `s3:CreateBucket`
- `s3:PutObject`
- `s3:GetObject`
- `s3:ListBucket`
- `s3:PutBucketPolicy`
- `s3:PutBucketVersioning`
- `s3:PutEncryptionConfiguration`

### IAM
- `iam:CreateRole`
- `iam:PutRolePolicy`
- `iam:AttachRolePolicy`
- `iam:GetRole`
- `iam:PassRole`

### SSM (Parameter Store)
- `ssm:PutParameter`
- `ssm:GetParameter`

---

## 🎯 Quick Fix Command

After adding permissions in AWS Console, run:

```bash
# Clear any cached credentials
aws sts get-caller-identity

# Try bootstrap again
npx cdk bootstrap --verbose
```

---

## ✅ Expected Success Output

After fixing permissions, you should see:

```
 ⏳  Bootstrapping environment aws://793323451177/us-east-1...
Trusted accounts for deployment: (none)
Trusted accounts for lookup: (none)
Using default execution policy of 'arn:aws:iam::aws:policy/AdministratorAccess'.
CDKToolkit: creating CloudFormation changeset...
 ✅  Environment aws://793323451177/us-east-1 bootstrapped.
```

---

## 🚨 Still Getting Errors?

### Check if Permissions Propagated
Wait 1-2 minutes after adding permissions, then try again.

### Verify User
```bash
aws sts get-caller-identity
```

Should show:
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "793323451177",
    "Arn": "arn:aws:iam::793323451177:user/kiro-agent-deployer"
}
```

### Clear Credential Cache
```bash
# Windows (PowerShell)
Remove-Item -Path "$env:USERPROFILE\.aws\cli\cache" -Recurse -Force -ErrorAction SilentlyContinue

# Then try again
npx cdk bootstrap
```

---

## 📝 Step-by-Step Visual Guide

### Adding AdministratorAccess (Easiest)

1. **AWS Console** → https://console.aws.amazon.com/iam/
2. **Left Sidebar** → Click "Users"
3. **User List** → Click "kiro-agent-deployer"
4. **Permissions Tab** → Click "Add permissions"
5. **Grant Permissions** → Click "Attach policies directly"
6. **Search Box** → Type "AdministratorAccess"
7. **Checkbox** → Check "AdministratorAccess"
8. **Bottom Right** → Click "Add permissions"
9. **Confirmation** → You should see "AdministratorAccess" in the policies list

### Verify It Worked

```bash
# Run this - should work now
aws cloudformation describe-stacks

# If you get a list or "Stack not found" - permissions work!
# If you get "AccessDenied" - wait 1 minute and try again
```

---

## 🎓 Understanding the Error

**What happened:**
- CDK needs to create a CloudFormation stack called "CDKToolkit"
- To do this, it first checks if the stack exists (`DescribeStacks`)
- Your user doesn't have permission to check CloudFormation stacks
- So CDK can't proceed

**What you need:**
- CloudFormation permissions (to create the bootstrap stack)
- S3 permissions (to create the CDK assets bucket)
- IAM permissions (to create CDK execution roles)

**Easiest fix:**
- Add `AdministratorAccess` policy to your user (for testing)
- Or add specific policies listed in Option 2

---

## 💡 Pro Tips

1. **For Testing**: Use AdministratorAccess (Option 1)
2. **For Production**: Use specific policies (Option 2)
3. **For Security**: Create custom policy (Option 3)
4. **Can't Modify User**: Use different profile (Option 4)

---

## 🔐 Security Note

**AdministratorAccess** gives full access to your AWS account. This is fine for:
- ✅ Testing and development
- ✅ Personal AWS accounts
- ✅ Learning and experimentation

For production or shared accounts, use **Option 2** (specific policies) instead.

---

## ✅ After Bootstrap Succeeds

Once bootstrap works, you can deploy:

```bash
# Deploy the stack
npx cdk deploy

# You'll be asked to approve IAM changes
# Type 'y' and press Enter
```

---

## 📞 Need Help?

If you're still stuck after adding permissions:

1. **Wait 2 minutes** (permissions take time to propagate)
2. **Run**: `aws sts get-caller-identity` (verify you're using the right user)
3. **Run**: `npx cdk bootstrap --verbose` (see detailed error)
4. **Share**: The new error message if it's different

---

**Most likely fix**: Add `AdministratorAccess` policy to `kiro-agent-deployer` user in IAM Console, wait 1 minute, then run `npx cdk bootstrap` again! 🚀
