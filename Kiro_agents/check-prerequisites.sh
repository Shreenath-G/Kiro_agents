#!/bin/bash

echo "🔍 Checking Prerequisites for AI Agent Deployment"
echo "=================================================="
echo ""

# Check Node.js
echo "📦 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js installed: $NODE_VERSION"
    
    # Check if version is 18+
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo "   ✅ Version is 18 or higher"
    else
        echo "   ⚠️  Version should be 18 or higher"
    fi
else
    echo "❌ Node.js not found. Please install Node.js 18+"
fi

echo ""

# Check Python
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python installed: $PYTHON_VERSION"
else
    echo "❌ Python not found. Please install Python 3.9+"
fi

echo ""

# Check AWS CLI
echo "☁️  Checking AWS CLI..."
if command -v aws &> /dev/null; then
    AWS_VERSION=$(aws --version)
    echo "✅ AWS CLI installed: $AWS_VERSION"
else
    echo "❌ AWS CLI not found. Please install AWS CLI v2"
fi

echo ""

# Check AWS credentials
echo "🔑 Checking AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    REGION=$(aws configure get region)
    echo "✅ AWS credentials configured"
    echo "   Account: $ACCOUNT_ID"
    echo "   Region: $REGION"
else
    echo "❌ AWS credentials not configured. Run 'aws configure'"
fi

echo ""

# Check npm
echo "📦 Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm installed: $NPM_VERSION"
else
    echo "❌ npm not found"
fi

echo ""
echo "=================================================="
echo "Summary:"
echo ""

# Count checks
CHECKS_PASSED=0
CHECKS_TOTAL=5

command -v node &> /dev/null && ((CHECKS_PASSED++))
command -v python3 &> /dev/null && ((CHECKS_PASSED++))
command -v aws &> /dev/null && ((CHECKS_PASSED++))
aws sts get-caller-identity &> /dev/null && ((CHECKS_PASSED++))
command -v npm &> /dev/null && ((CHECKS_PASSED++))

echo "Checks passed: $CHECKS_PASSED/$CHECKS_TOTAL"
echo ""

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo "✅ All prerequisites met! Ready to deploy."
    echo ""
    echo "Next steps:"
    echo "1. npm install"
    echo "2. npx cdk bootstrap (first time only)"
    echo "3. npx cdk deploy"
else
    echo "⚠️  Some prerequisites missing. Please install them first."
    echo ""
    echo "Installation guides:"
    echo "- Node.js: https://nodejs.org/"
    echo "- Python: https://www.python.org/"
    echo "- AWS CLI: https://aws.amazon.com/cli/"
fi
