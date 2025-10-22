@echo off
REM CDK Bootstrap Diagnostic Script for Windows CMD
REM Run this to diagnose bootstrap issues

echo ========================================
echo CDK Bootstrap Diagnostic Tool
echo ========================================
echo.

REM Check 1: Node.js
echo 1. Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] Node.js installed
    node --version
) else (
    echo    [ERROR] Node.js not found
    echo    Install from: https://nodejs.org/
)
echo.

REM Check 2: npm
echo 2. Checking npm...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] npm installed
    npm --version
) else (
    echo    [ERROR] npm not found
)
echo.

REM Check 3: AWS CLI
echo 3. Checking AWS CLI...
aws --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] AWS CLI installed
    aws --version
) else (
    echo    [ERROR] AWS CLI not found
    echo    Install from: https://aws.amazon.com/cli/
)
echo.

REM Check 4: AWS Credentials
echo 4. Checking AWS Credentials...
aws sts get-caller-identity >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] AWS credentials configured
    aws sts get-caller-identity --query Account --output text
) else (
    echo    [ERROR] AWS credentials not configured
    echo    Run: aws configure
)
echo.

REM Check 5: AWS Region
echo 5. Checking AWS Region...
aws configure get region >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] Region configured
    aws configure get region
) else (
    echo    [ERROR] Region not configured
    echo    Run: aws configure set region us-east-1
)
echo.

REM Check 6: Project Files
echo 6. Checking Project Files...
if exist cdk.json (
    echo    [OK] cdk.json found
) else (
    echo    [ERROR] cdk.json not found
    echo    Make sure you're in the project root directory
)

if exist package.json (
    echo    [OK] package.json found
) else (
    echo    [ERROR] package.json not found
)

if exist lib\ai-agent-stack.ts (
    echo    [OK] ai-agent-stack.ts found
) else (
    echo    [ERROR] ai-agent-stack.ts not found
)
echo.

REM Check 7: Node Modules
echo 7. Checking Dependencies...
if exist node_modules (
    echo    [OK] node_modules directory exists
    if exist node_modules\aws-cdk-lib (
        echo    [OK] aws-cdk-lib installed
    ) else (
        echo    [ERROR] aws-cdk-lib not installed
        echo    Run: npm install
    )
) else (
    echo    [ERROR] node_modules not found
    echo    Run: npm install
)
echo.

REM Check 8: CDK
echo 8. Checking CDK...
npx cdk --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] CDK available
    npx cdk --version
) else (
    echo    [ERROR] CDK not available
    echo    Run: npm install
)
echo.

echo ========================================
echo Summary
echo ========================================
echo.
echo If all checks passed, run:
echo   npx cdk bootstrap
echo.
echo If any checks failed, fix them first.
echo See TROUBLESHOOTING.md for detailed help.
echo.

pause
