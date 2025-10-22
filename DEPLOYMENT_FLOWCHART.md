# Deployment & Working Flowchart

## 🎯 Visual Guide: From Zero to Working Agent

This document provides visual flowcharts for the entire deployment and operation process.

---

## 📊 Complete Deployment Flow

```
START
  │
  ├─→ [1] Prerequisites Setup (10 min)
  │    ├─ Install Node.js 18+
  │    ├─ Install Python 3.9+
  │    ├─ Install AWS CLI v2
  │    └─ Install Git (optional)
  │
  ├─→ [2] AWS Account Setup (15 min)
  │    ├─ Create AWS Account
  │    ├─ Create IAM User
  │    ├─ Generate Access Keys
  │    ├─ Configure AWS CLI
  │    └─ Enable Bedrock Nova Pro
  │
  ├─→ [3] Project Setup (5 min)
  │    ├─ Download/Clone Project
  │    ├─ Verify File Structure
  │    └─ Run: npm install
  │
  ├─→ [4] Deployment (10 min)
  │    ├─ Run: npx cdk bootstrap
  │    ├─ Run: npx cdk deploy
  │    └─ Save Agent ID
  │
  ├─→ [5] Agent Configuration (5 min)
  │    ├─ Open Bedrock Console
  │    ├─ Create Agent Alias
  │    └─ Save Alias ID
  │
  ├─→ [6] Testing (5 min)
  │    ├─ Run: python test-agent.py
  │    └─ Run: python interactive-demo.py
  │
  └─→ SUCCESS! Agent is Working ✅
```

**Total Time**: 30-50 minutes

---

## 🔄 Agent Working Flow

### User Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│  Types: "Optimize my campaigns to maximize ROI"             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              BEDROCK AGENT (Nova Pro)                        │
│                                                              │
│  Step 1: Understand Intent                                  │
│  "User wants to optimize campaigns for ROI"                 │
│                                                              │
│  Step 2: Plan Approach                                      │
│  "I need to: get campaigns → analyze → optimize → execute"  │
│                                                              │
│  Step 3: Reason About Tools                                 │
│  "I'll use google_ads, meta_ads, analytics, budget_optimizer"│
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   TOOL ORCHESTRATION                         │
│                                                              │
│  [1] google_ads.get_campaigns()                             │
│      └─→ Returns: 3 Google campaigns                        │
│                                                              │
│  [2] meta_ads.get_campaigns()                               │
│      └─→ Returns: 3 Meta campaigns                          │
│                                                              │
│  [3] analytics.analyze_performance(each campaign)           │
│      └─→ Returns: Performance metrics, issues, trends       │
│                                                              │
│  [4] budget_optimizer.optimize(total_budget, campaigns)     │
│      └─→ Returns: Optimal allocation recommendations        │
│                                                              │
│  [5] google_ads.update_budget(campaign_id, new_budget)      │
│      └─→ Returns: Success confirmation                      │
│                                                              │
│  [6] meta_ads.update_budget(campaign_id, new_budget)        │
│      └─→ Returns: Success confirmation                      │
│                                                              │
│  [7] storage.store(key, decision_data)                      │
│      └─→ Returns: Stored successfully                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  AGENT SYNTHESIS                             │
│                                                              │
│  Combines all information:                                  │
│  - Campaign performance data                                │
│  - Optimization decisions made                              │
│  - Expected outcomes                                        │
│  - Recommendations                                          │
│                                                              │
│  Generates human-readable response                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER RESPONSE                             │
│                                                              │
│  "I've optimized your campaigns:                            │
│   - Reduced budget on goog-camp-002 by $300                 │
│   - Increased budget on goog-camp-001 by $300               │
│   - Expected ROAS improvement: 1.68x → 2.85x                │
│   - Estimated additional revenue: +$6,500/month"            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Detailed Lambda Function Flow

### Example: Google Ads Lambda Function

```
┌─────────────────────────────────────────────────────────────┐
│  BEDROCK AGENT                                              │
│  Calls: google_ads.get_campaigns()                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS LAMBDA: GoogleAdsFunction                              │
│                                                              │
│  1. Receive Event                                           │
│     {                                                        │
│       "apiPath": "/campaigns",                              │
│       "httpMethod": "GET",                                  │
│       "actionGroup": "google-ads-actions"                   │
│     }                                                        │
│                                                              │
│  2. Parse Request                                           │
│     - Extract API path                                      │
│     - Extract HTTP method                                   │
│     - Extract parameters                                    │
│                                                              │
│  3. Execute Logic                                           │
│     if path == "/campaigns" and method == "GET":            │
│         campaigns = get_campaigns()                         │
│                                                              │
│  4. Get Campaign Data                                       │
│     - Query DynamoDB for metrics                            │
│     - Or call Google Ads API (production)                   │
│     - Or return simulated data (demo)                       │
│                                                              │
│  5. Format Response                                         │
│     {                                                        │
│       "campaigns": [                                        │
│         {                                                    │
│           "id": "goog-camp-001",                            │
│           "name": "Search - Brand Keywords",                │
│           "budget": 1500,                                   │
│           "status": "ENABLED"                               │
│         },                                                   │
│         ...                                                  │
│       ]                                                      │
│     }                                                        │
│                                                              │
│  6. Return to Agent                                         │
│     {                                                        │
│       "messageVersion": "1.0",                              │
│       "response": {                                         │
│         "httpStatusCode": 200,                              │
│         "responseBody": {...}                               │
│       }                                                      │
│     }                                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  BEDROCK AGENT                                              │
│  Receives campaign data                                     │
│  Continues with next tool call                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
├─────────────────────────────────────────────────────────────┤
│  • Google Ads API (future)                                  │
│  • Meta Ads API (future)                                    │
│  • Simulated Data (demo)                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  LAMBDA FUNCTIONS                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Google Ads   │  │  Meta Ads    │  │  Analytics   │     │
│  │   Lambda     │  │   Lambda     │  │   Lambda     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │              │
│         └─────────────────┴──────────────────┘              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  DATA STORAGE                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DYNAMODB: ad-optimizer-metrics                      │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │ campaignId | timestamp | impressions | clicks  │  │  │
│  │  │ goog-001   | 167...    | 45000       | 2250    │  │  │
│  │  │ goog-002   | 167...    | 120000      | 960     │  │  │
│  │  │ meta-001   | 167...    | 85000       | 3400    │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │  TTL: 90 days (auto-cleanup)                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  S3: ad-optimizer-data-{account}                     │  │
│  │  ├── insights/                                       │  │
│  │  │   ├── optimization-2024-01-15.json               │  │
│  │  │   ├── decision-log-2024-01-16.json               │  │
│  │  │   └── ...                                         │  │
│  │  └── campaigns/                                      │  │
│  │      ├── goog-camp-001/                              │  │
│  │      └── meta-camp-001/                              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  BEDROCK AGENT                               │
│  Uses data for reasoning and decision-making                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Autonomous Optimization Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTINUOUS MONITORING                     │
│  (EventBridge triggers every hour)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Collect Metrics                                    │
│  ├─ Get all campaigns                                       │
│  ├─ Query latest metrics from DynamoDB                      │
│  └─ Calculate current performance                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Detect Issues                                      │
│  ├─ Check for CTR decline (ad fatigue)                      │
│  ├─ Check for CPA increase (efficiency drop)                │
│  ├─ Check for ROAS below target                             │
│  └─ Check for market volatility (CPM changes)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                    ┌────┴────┐
                    │ Issues? │
                    └────┬────┘
                         │
            ┌────────────┼────────────┐
            │ YES                     │ NO
            ▼                         ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│  STEP 3: Take Action    │  │  Continue Monitoring    │
│  ├─ Adjust bids         │  │  └─ Log: "All good"     │
│  ├─ Reallocate budget   │  └─────────────────────────┘
│  ├─ Pause poor ads      │
│  ├─ Activate backups    │
│  └─ Store decision      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Verify Results                                     │
│  ├─ Wait 24 hours                                           │
│  ├─ Check if performance improved                           │
│  └─ Adjust strategy if needed                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Learn & Adapt                                      │
│  ├─ Store outcome in S3                                     │
│  ├─ Update optimization strategy                            │
│  └─ Improve future decisions                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         └─→ LOOP BACK TO STEP 1
```

---

## 🎯 Decision Tree: Budget Optimization

```
START: Optimize Budget
         │
         ▼
    Get All Campaigns
         │
         ▼
    Calculate Current ROAS
         │
         ▼
    ┌────────────────┐
    │ Any campaign   │
    │ ROAS < 1.0?    │
    └────┬───────────┘
         │
    ┌────┴────┐
    │ YES     │ NO
    ▼         ▼
┌─────────┐  ┌─────────────────┐
│ Reduce  │  │ Check for       │
│ Budget  │  │ High Performers │
│ by 30%  │  │ (ROAS > 3.0)    │
└────┬────┘  └────┬────────────┘
     │            │
     │            ▼
     │       ┌────────────────┐
     │       │ Any campaign   │
     │       │ ROAS > 3.0?    │
     │       └────┬───────────┘
     │            │
     │       ┌────┴────┐
     │       │ YES     │ NO
     │       ▼         ▼
     │  ┌─────────┐  ┌──────────────┐
     │  │Increase │  │ Maintain     │
     │  │Budget   │  │ Current      │
     │  │by 20%   │  │ Allocation   │
     │  └────┬────┘  └──────────────┘
     │       │
     └───────┴───────────┐
                         │
                         ▼
              ┌──────────────────┐
              │ Calculate Total  │
              │ Expected ROAS    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Store Decision   │
              │ in S3            │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Execute Changes  │
              │ via Lambda       │
              └────────┬─────────┘
                       │
                       ▼
                     SUCCESS
```

---

## 📈 Performance Metrics Flow

```
Campaign Running
      │
      ▼
┌─────────────────┐
│ Metrics         │
│ Generated       │
│ - Impressions   │
│ - Clicks        │
│ - Conversions   │
│ - Cost          │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Lambda Function Collects            │
│ (Every hour or on-demand)           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Calculate Derived Metrics           │
│ - CTR = (Clicks / Impressions) × 100│
│ - CPC = Cost / Clicks               │
│ - CPA = Cost / Conversions          │
│ - ROAS = Revenue / Cost             │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Store in DynamoDB                   │
│ {                                   │
│   campaignId: "goog-camp-001",      │
│   timestamp: 1234567890,            │
│   ctr: 5.0,                         │
│   cpa: 8.06,                        │
│   roas: 6.21,                       │
│   ttl: 1234567890 + (90 days)       │
│ }                                   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Analytics Lambda Analyzes           │
│ - Compare to historical data        │
│ - Detect trends                     │
│ - Identify anomalies                │
│ - Generate insights                 │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Agent Uses for Decision-Making      │
│ - Optimize budget                   │
│ - Adjust bids                       │
│ - Refresh creatives                 │
└─────────────────────────────────────┘
```

---

## 🔐 Security Flow

```
┌─────────────────────────────────────┐
│ User Credentials                    │
│ (AWS Access Keys)                   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ AWS CLI Configuration               │
│ ~/.aws/credentials                  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ IAM User                            │
│ - AdministratorAccess (setup)      │
│ - Or custom policy (production)    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ CDK Deployment                      │
│ - Creates IAM roles                 │
│ - Least privilege access            │
└────────┬────────────────────────────┘
         │
         ├─→ BedrockAgentRole
         │   └─ Can invoke Lambda functions
         │
         ├─→ GoogleAdsFunctionRole
         │   ├─ Can read/write DynamoDB
         │   ├─ Can read/write S3
         │   └─ Can read Secrets Manager
         │
         ├─→ MetaAdsFunctionRole
         │   └─ (Same permissions)
         │
         └─→ AnalyticsFunctionRole
             └─ (Read-only DynamoDB)
```

---

## 💰 Cost Flow

```
User Activity
      │
      ▼
┌─────────────────────────────────────┐
│ Bedrock Agent Invocation            │
│ Cost: $0.008 per 1K input tokens    │
│       $0.032 per 1K output tokens   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Lambda Function Executions          │
│ Cost: $0.20 per 1M requests         │
│       + compute time                │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ DynamoDB Operations                 │
│ Cost: Pay-per-request               │
│       ~$1.25 per 1M writes          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ S3 Storage                          │
│ Cost: $0.023 per GB/month           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Total Monthly Cost                  │
│ Moderate Usage: ~$25/month          │
│ - Bedrock: $15                      │
│ - Lambda: $5                        │
│ - DynamoDB: $3                      │
│ - S3: $2                            │
└─────────────────────────────────────┘
```

---

## ✅ Success Validation Flow

```
Deployment Complete
      │
      ▼
┌─────────────────────────────────────┐
│ Check 1: Resources Created?         │
│ aws lambda list-functions           │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │ YES     │ NO → Troubleshoot
    ▼         
┌─────────────────────────────────────┐
│ Check 2: Agent Exists?              │
│ aws bedrock-agent list-agents       │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │ YES     │ NO → Wait 2 min, retry
    ▼         
┌─────────────────────────────────────┐
│ Check 3: Agent Responds?            │
│ Test in AWS Console                 │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │ YES     │ NO → Check logs
    ▼         
┌─────────────────────────────────────┐
│ Check 4: Python Tests Pass?        │
│ python test-agent.py                │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │ YES     │ NO → Check Agent ID
    ▼         
┌─────────────────────────────────────┐
│ Check 5: Interactive Demo Works?   │
│ python interactive-demo.py          │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │ YES     │ NO → Review errors
    ▼         
┌─────────────────────────────────────┐
│ ✅ SUCCESS!                         │
│ Agent is fully operational          │
└─────────────────────────────────────┘
```

---

**Use these flowcharts alongside STEP_BY_STEP_GUIDE.md for complete understanding!** 🎯
