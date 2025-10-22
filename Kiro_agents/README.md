# AWS AI Advertisement Optimization Agent

> A production-ready autonomous AI agent that optimizes Google Ads and Meta Ads campaigns for small businesses

[![AWS](https://img.shields.io/badge/AWS-Bedrock-orange)](https://aws.amazon.com/bedrock/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-CDK-blue)](https://aws.amazon.com/cdk/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Overview

An intelligent advertising agent that autonomously optimizes ad campaigns, adjusts budgets, tests creatives, and maximizes ROI for small businesses. Built with Amazon Bedrock's Nova Pro model for advanced reasoning and decision-making.

## 💡 The Problem

Most small business owners are experts in their product, **not in digital advertising**. They face:

- ❌ Hours spent manually tweaking campaigns with gut feelings
- ❌ Expensive agencies ($2,000-$10,000/month)
- ❌ Simple rule-based tools that can't adapt to market changes
- ❌ Ad fatigue, competitor actions, and platform algorithm changes
- ❌ Significant financial waste and missed opportunities

## ✨ The Solution

An **autonomous AI agent** that:

- ✅ Monitors campaign performance 24/7
- ✅ Automatically adjusts bids, budgets, and targeting
- ✅ Tests ad creatives and identifies winners
- ✅ Adapts to market volatility and competitor actions
- ✅ Provides actionable insights and recommendations
- ✅ Learns from your business goals and constraints

### Key Capabilities

- 🤖 **Autonomous Optimization**: Makes independent decisions about bid adjustments, budget allocation, and targeting
- 🧠 **Advanced Reasoning**: Uses Nova Pro to understand campaign performance and market dynamics
- 🔧 **Multi-Platform Integration**: Google Ads API, Meta Ads API, and analytics tools
- 📊 **Performance Analysis**: Analyzes metrics, identifies trends, and predicts outcomes
- 💰 **Budget Management**: Automatically reallocates budget to high-performing campaigns
- 🎨 **Creative Testing**: A/B tests ad creatives and identifies winning variations

## 🏗️ Architecture

```
Small Business Owner → Bedrock Agent (Nova Pro) → Action Groups → Tools
                                                      ├─ Google Ads API (Lambda)
                                                      ├─ Meta Ads API (Lambda)
                                                      ├─ Performance Analytics (Lambda)
                                                      ├─ Budget Optimizer (Lambda)
                                                      └─ Campaign Data Storage (S3)
```

### AWS Services Used

- **Amazon Bedrock Agents**: Core agent framework
- **Amazon Bedrock Nova Pro**: Reasoning LLM for campaign optimization
- **AWS Lambda**: Serverless tool execution (5 functions)
- **Amazon S3**: Campaign data, performance history, and insights storage
- **Amazon DynamoDB**: Real-time campaign metrics and state management
- **AWS Secrets Manager**: Secure API key storage for Google/Meta
- **Amazon EventBridge**: Scheduled optimization runs
- **AWS IAM**: Security and permissions
- **AWS CDK**: Infrastructure as Code

## ✨ Features

### 1. Autonomous Campaign Optimization
```
Agent monitors: Campaign performance drops by 15%
Agent analyzes: Ad fatigue detected, CTR declining
Agent decides: Pause underperforming ads, increase budget on winners
Agent executes: Adjusts bids, reallocates budget, activates backup creatives
Result: Performance restored, ROI improved by 23%
```

### 2. Intelligent Budget Allocation
```
Agent detects: Campaign A has 3x ROAS, Campaign B has 0.8x ROAS
Agent reasons: Shift budget from B to A while testing new angles for B
Agent executes: Reallocates 40% of budget, maintains minimum spend on B
Result: Overall ROAS increases from 1.5x to 2.1x
```

### 3. Creative Performance Testing
```
Agent runs: A/B test on 5 ad variations
Agent analyzes: Variation 3 has 2.5x higher conversion rate
Agent decides: Scale winning creative, pause losers, generate similar variants
Result: Cost per acquisition drops by 35%
```

### 4. Market Adaptation
```
Agent monitors: Competitor increases ad spend, CPM rises 40%
Agent reasons: Market becoming more competitive, need strategic response
Agent executes: Adjusts targeting, tests new audiences, optimizes ad schedule
Result: Maintains performance despite market changes
```

### 5. Multi-Platform Orchestration
```
User goal: "Maximize conversions with $5,000/month budget across Google and Meta"
Agent: Analyzes both platforms → Identifies best opportunities → Allocates budget dynamically
Result: Optimal spend distribution, unified reporting, cross-platform insights
```

## 🚀 Quick Start

### Prerequisites

```bash
# Check prerequisites
./check-prerequisites.sh
```

Required:
- AWS Account with Bedrock access
- Node.js 18+
- Python 3.9+
- AWS CLI v2 configured

### Deploy in 3 Steps

```bash
# 1. Install dependencies
npm install

# 2. Bootstrap CDK (first time only)
npx cdk bootstrap

# 3. Deploy
npx cdk deploy
```

### Enable Bedrock Access

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock)
2. Click "Model access" → "Manage model access"
3. Enable "Nova Pro"
4. Wait for approval (usually instant)

### Configure API Keys (Optional for Demo)

After deployment, update the API keys in AWS Secrets Manager:

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

**Note**: The agent works with simulated data for demo purposes. Add real API keys to connect to actual campaigns.

### Create Agent Alias

1. Go to Bedrock Agents console
2. Select "ad-optimizer-agent"
3. Create alias named "production"
4. Note Agent ID and Alias ID

### Test Your Agent

```bash
# Automated tests
python test-agent.py

# Interactive chat
python interactive-demo.py
```

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 10 minutes
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment guide
- **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - Presentation guide
- **[REQUIREMENTS_COMPLIANCE.md](REQUIREMENTS_COMPLIANCE.md)** - Competition requirements
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project overview

## 🎮 Example Usage

### Campaign Overview
```
"Show me all my campaigns and their current performance"
```

### Performance Analysis
```
"Analyze campaign goog-camp-001 and identify any issues"
```

### Budget Optimization
```
"I have $5000/month budget. Optimize allocation across all campaigns to maximize ROAS"
```

### Autonomous Optimization
```
"Find my worst performing campaign and take action to improve it. 
Reduce its budget and reallocate to better performers."
```

### Cross-Platform Analysis
```
"Compare Google Ads vs Meta Ads. Which platform gives better ROI?"
```

### Creative Testing
```
"Which Meta campaign needs new creatives? Set up an A/B test."
```

### Trend Detection
```
"Are any campaigns showing signs of ad fatigue? What should I do?"
```

## 🏆 Competition Requirements

### ✅ All Requirements Met

1. **LLM on AWS**: Amazon Bedrock Nova Pro
2. **AWS Services**: Bedrock Agents, Nova, Lambda, S3
3. **AI Agent Qualifications**:
   - ✅ Reasoning LLM for decision-making
   - ✅ Autonomous capabilities
   - ✅ External tool integration (3+ tools)
   - ✅ Multi-tool orchestration

See [REQUIREMENTS_COMPLIANCE.md](REQUIREMENTS_COMPLIANCE.md) for details.

## 📁 Project Structure

```
aws-ai-research-agent/
├── bin/app.ts                    # CDK entry point
├── lib/ai-agent-stack.ts         # Infrastructure stack
├── lambda/                       # Tool implementations
│   ├── web-search/
│   ├── code-execution/
│   └── storage/
├── test-agent.py                 # Automated tests
├── interactive-demo.py           # Chat interface
└── docs/                         # Documentation
```

## 🔒 Security

- IAM roles with least privilege
- Sandboxed code execution
- Encrypted S3 storage
- No hardcoded credentials
- VPC isolation (optional)

## 💰 Cost Estimate

**Moderate Usage**: ~$15-20/month
- Bedrock Nova Pro: ~$10-15
- Lambda: ~$2-3
- S3: ~$1-2

**Testing**: < $1/hour

## 🔧 Customization

### Add New Tools

1. Create Lambda function
2. Define OpenAPI spec
3. Add Action Group
4. Deploy

### Modify Behavior

Edit agent instructions in `lib/ai-agent-stack.ts`:
```typescript
instruction: `Your custom instructions here...`
```

## 📊 Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/lambda/AIResearchAgentStack-WebSearchFunction --follow
```

### S3 Contents
```bash
aws s3 ls s3://ai-agent-knowledge-YOUR_ACCOUNT/research/
```

### Agent Metrics
View in Bedrock Agents console → Metrics tab

## 🧪 Testing

### Run All Tests
```bash
python test-agent.py
```

### Interactive Mode
```bash
python interactive-demo.py
```

### Manual Testing
Use AWS Console → Bedrock → Agents → Test tab

## 🗑️ Cleanup

```bash
npx cdk destroy
```

Removes all resources and stops charges.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Real web search API integration
- Vector database for semantic search
- Additional tools (email, database, etc.)
- Advanced reasoning chains
- Multi-agent collaboration

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- Amazon Bedrock and Nova Pro
- AWS CDK
- AWS Lambda
- Amazon S3

## 📞 Support

- Check documentation in project root
- Review CloudWatch logs for debugging
- See [DEPLOYMENT.md](DEPLOYMENT.md) for troubleshooting
- AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/

## 🎯 Next Steps

1. ✅ Deploy the agent
2. ✅ Run tests
3. ✅ Try example prompts
4. ✅ Customize for your use case
5. ✅ Add new tools
6. ✅ Deploy to production

---

**Built with AWS. Powered by Nova. Ready to deploy.** 🚀
