#!/bin/bash

echo "🚀 Deploying AI Research Assistant Agent to AWS"
echo "================================================"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS CLI configured"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Bootstrap CDK (if not already done)
echo ""
echo "🔧 Bootstrapping CDK..."
npx cdk bootstrap

# Deploy the stack
echo ""
echo "🚀 Deploying stack..."
npx cdk deploy --require-approval never

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Go to AWS Console > Amazon Bedrock > Agents"
echo "2. Find your 'research-assistant-agent'"
echo "3. Create an alias for the agent"
echo "4. Test the agent using the test-agent.py script"
echo ""
echo "Run: python test-agent.py"
