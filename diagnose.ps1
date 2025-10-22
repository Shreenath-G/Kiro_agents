# CDK Bootstrap Diagnostic Script
# Run this in PowerShell to diagnose issues

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CDK Bootstrap Diagnostic Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Node.js
Write-Host "1. Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "   ✓ Node.js installed: $nodeVersion" -ForegroundColor Green
    
    $nodeMajor = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
    if ($nodeMajor -ge 18) {
        Write-Host "   ✓ Version is 18 or higher" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Version should be 18 or higher" -ForegroundColor Red
    }
} catch {
    Write-Host "   ✗ Node.js not found" -ForegroundColor Red
    Write-Host "   Install from: https://nodejs.org/" -ForegroundColor Yellow
}
Write-Host ""

# Check 2: npm
Write-Host "2. Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "   ✓ npm installed: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ npm not found" -ForegroundColor Red
}
Write-Host ""

# Check 3: AWS CLI
Write-Host "3. Checking AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version
    Write-Host "   ✓ AWS CLI installed: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ AWS CLI not found" -ForegroundColor Red
    Write-Host "   Install from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
}
Write-Host ""

# Check 4: AWS Credentials
Write-Host "4. Checking AWS Credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ AWS credentials configured" -ForegroundColor Green
        $identityJson = $identity | ConvertFrom-Json
        Write-Host "   Account: $($identityJson.Account)" -ForegroundColor Cyan
        Write-Host "   User: $($identityJson.Arn)" -ForegroundColor Cyan
    } else {
        Write-Host "   ✗ AWS credentials not configured" -ForegroundColor Red
        Write-Host "   Run: aws configure" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Cannot verify AWS credentials" -ForegroundColor Red
    Write-Host "   Run: aws configure" -ForegroundColor Yellow
}
Write-Host ""

# Check 5: AWS Region
Write-Host "5. Checking AWS Region..." -ForegroundColor Yellow
try {
    $region = aws configure get region
    if ($region) {
        Write-Host "   ✓ Region configured: $region" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Region not configured" -ForegroundColor Red
        Write-Host "   Run: aws configure set region us-east-1" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Cannot check region" -ForegroundColor Red
}
Write-Host ""

# Check 6: Project Directory
Write-Host "6. Checking Project Files..." -ForegroundColor Yellow
if (Test-Path "cdk.json") {
    Write-Host "   ✓ cdk.json found" -ForegroundColor Green
} else {
    Write-Host "   ✗ cdk.json not found" -ForegroundColor Red
    Write-Host "   Make sure you're in the project root directory" -ForegroundColor Yellow
}

if (Test-Path "package.json") {
    Write-Host "   ✓ package.json found" -ForegroundColor Green
} else {
    Write-Host "   ✗ package.json not found" -ForegroundColor Red
}

if (Test-Path "lib/ai-agent-stack.ts") {
    Write-Host "   ✓ ai-agent-stack.ts found" -ForegroundColor Green
} else {
    Write-Host "   ✗ ai-agent-stack.ts not found" -ForegroundColor Red
}
Write-Host ""

# Check 7: Node Modules
Write-Host "7. Checking Dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Write-Host "   ✓ node_modules directory exists" -ForegroundColor Green
    
    if (Test-Path "node_modules/aws-cdk-lib") {
        Write-Host "   ✓ aws-cdk-lib installed" -ForegroundColor Green
    } else {
        Write-Host "   ✗ aws-cdk-lib not installed" -ForegroundColor Red
        Write-Host "   Run: npm install" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ✗ node_modules not found" -ForegroundColor Red
    Write-Host "   Run: npm install" -ForegroundColor Yellow
}
Write-Host ""

# Check 8: CDK
Write-Host "8. Checking CDK..." -ForegroundColor Yellow
try {
    $cdkVersion = npx cdk --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ CDK available: $cdkVersion" -ForegroundColor Green
    } else {
        Write-Host "   ✗ CDK not available" -ForegroundColor Red
        Write-Host "   Run: npm install" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Cannot check CDK" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary & Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check if all prerequisites are met
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Install Node.js 18+" -ForegroundColor Red
    $allGood = $false
}

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Install AWS CLI v2" -ForegroundColor Red
    $allGood = $false
}

try {
    aws sts get-caller-identity 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Configure AWS credentials: aws configure" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "❌ Configure AWS credentials: aws configure" -ForegroundColor Red
    $allGood = $false
}

if (-not (Test-Path "cdk.json")) {
    Write-Host "❌ Navigate to project root directory" -ForegroundColor Red
    $allGood = $false
}

if (-not (Test-Path "node_modules")) {
    Write-Host "❌ Install dependencies: npm install" -ForegroundColor Red
    $allGood = $false
}

if ($allGood) {
    Write-Host "✅ All checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready to bootstrap! Run:" -ForegroundColor Cyan
    Write-Host "  npx cdk bootstrap" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Fix the issues above, then run:" -ForegroundColor Yellow
    Write-Host "  npx cdk bootstrap" -ForegroundColor White
    Write-Host ""
}

Write-Host "For detailed troubleshooting, see: TROUBLESHOOTING.md" -ForegroundColor Cyan
Write-Host ""
