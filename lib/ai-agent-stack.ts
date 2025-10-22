import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as bedrock from 'aws-cdk-lib/aws-bedrock';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import * as path from 'path';

export class AIAgentStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket for campaign data and performance history
    const campaignDataBucket = new s3.Bucket(this, 'CampaignDataBucket', {
      bucketName: `ad-optimizer-data-${this.account}`,
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      lifecycleRules: [
        {
          expiration: cdk.Duration.days(90),
          transitions: [
            {
              storageClass: s3.StorageClass.INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(30),
            },
          ],
        },
      ],
    });

    // DynamoDB table for real-time campaign metrics
    const metricsTable = new dynamodb.Table(this, 'CampaignMetricsTable', {
      tableName: 'ad-optimizer-metrics',
      partitionKey: { name: 'campaignId', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'timestamp', type: dynamodb.AttributeType.NUMBER },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      timeToLiveAttribute: 'ttl',
      pointInTimeRecovery: true,
    });

    // Secrets Manager for API keys
    const apiKeysSecret = new secretsmanager.Secret(this, 'AdPlatformAPIKeys', {
      secretName: 'ad-optimizer/api-keys',
      description: 'API keys for Google Ads and Meta Ads',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          googleAdsClientId: 'REPLACE_WITH_YOUR_CLIENT_ID',
          googleAdsClientSecret: 'REPLACE_WITH_YOUR_CLIENT_SECRET',
          googleAdsRefreshToken: 'REPLACE_WITH_YOUR_REFRESH_TOKEN',
          googleAdsDeveloperToken: 'REPLACE_WITH_YOUR_DEVELOPER_TOKEN',
          metaAccessToken: 'REPLACE_WITH_YOUR_META_ACCESS_TOKEN',
          metaAdAccountId: 'REPLACE_WITH_YOUR_AD_ACCOUNT_ID',
        }),
        generateStringKey: 'placeholder',
      },
    });

    // Lambda function for Google Ads integration
    const googleAdsFunction = new lambda.Function(this, 'GoogleAdsFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/google-ads')),
      timeout: cdk.Duration.seconds(120), // Increased for Nova Pro compatibility
      memorySize: 1024, // Increased to reduce cold starts
      environment: {
        BUCKET_NAME: campaignDataBucket.bucketName,
        METRICS_TABLE: metricsTable.tableName,
        SECRETS_ARN: apiKeysSecret.secretArn,
      },
    });

    campaignDataBucket.grantReadWrite(googleAdsFunction);
    metricsTable.grantReadWriteData(googleAdsFunction);
    apiKeysSecret.grantRead(googleAdsFunction);

    // Lambda function for Meta Ads integration
    const metaAdsFunction = new lambda.Function(this, 'MetaAdsFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/meta-ads')),
      timeout: cdk.Duration.seconds(120), // Increased for Nova Pro compatibility
      memorySize: 1024, // Increased to reduce cold starts
      environment: {
        BUCKET_NAME: campaignDataBucket.bucketName,
        METRICS_TABLE: metricsTable.tableName,
        SECRETS_ARN: apiKeysSecret.secretArn,
      },
    });

    campaignDataBucket.grantReadWrite(metaAdsFunction);
    metricsTable.grantReadWriteData(metaAdsFunction);
    apiKeysSecret.grantRead(metaAdsFunction);

    // Lambda function for performance analytics
    const analyticsFunction = new lambda.Function(this, 'AnalyticsFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/analytics')),
      timeout: cdk.Duration.seconds(90),
      memorySize: 1024,
      environment: {
        BUCKET_NAME: campaignDataBucket.bucketName,
        METRICS_TABLE: metricsTable.tableName,
      },
    });

    campaignDataBucket.grantReadWrite(analyticsFunction);
    metricsTable.grantReadData(analyticsFunction);

    // Lambda function for budget optimization
    const budgetOptimizerFunction = new lambda.Function(this, 'BudgetOptimizerFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/budget-optimizer')),
      timeout: cdk.Duration.seconds(120), // Increased for Nova Pro compatibility
      memorySize: 1024, // Increased to reduce cold starts
      environment: {
        BUCKET_NAME: campaignDataBucket.bucketName,
        METRICS_TABLE: metricsTable.tableName,
      },
    });

    campaignDataBucket.grantReadWrite(budgetOptimizerFunction);
    metricsTable.grantReadWriteData(budgetOptimizerFunction);

    // Lambda function for campaign data storage
    const storageFunction = new lambda.Function(this, 'StorageFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/storage')),
      timeout: cdk.Duration.seconds(30),
      environment: {
        BUCKET_NAME: campaignDataBucket.bucketName,
        METRICS_TABLE: metricsTable.tableName,
      },
    });

    campaignDataBucket.grantReadWrite(storageFunction);
    metricsTable.grantReadWriteData(storageFunction);

    // IAM role for Bedrock Agent
    const agentRole = new iam.Role(this, 'BedrockAgentRole', {
      assumedBy: new iam.ServicePrincipal('bedrock.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonBedrockFullAccess'),
      ],
    });

    // Grant agent permission to invoke Lambda functions
    googleAdsFunction.grantInvoke(agentRole);
    metaAdsFunction.grantInvoke(agentRole);
    analyticsFunction.grantInvoke(agentRole);
    budgetOptimizerFunction.grantInvoke(agentRole);
    storageFunction.grantInvoke(agentRole);

    // Create Bedrock Agent with Claude 3.5 Sonnet v2 (more reliable than Nova Pro)
    const agent = new bedrock.CfnAgent(this, 'AdOptimizerAgent', {
      agentName: 'ad-optimizer-agent',
      agentResourceRoleArn: agentRole.roleArn,
      foundationModel: 'anthropic.claude-3-5-sonnet-20241022-v2:0',
      instruction: `You are an expert digital advertising optimization agent for small businesses.
Your role is to autonomously optimize Google Ads and Meta Ads campaigns to maximize ROI.

You have access to five tools:
1. google_ads: Manage Google Ads campaigns (get metrics, adjust bids, update budgets, pause/activate ads)
2. meta_ads: Manage Meta Ads campaigns (get metrics, adjust bids, update budgets, pause/activate ads)
3. analytics: Analyze campaign performance, identify trends, and predict outcomes
4. budget_optimizer: Optimize budget allocation across campaigns and platforms
5. storage: Store insights, decisions, and performance history

Your responsibilities:
- Monitor campaign performance continuously
- Identify underperforming ads and campaigns
- Detect ad fatigue, market changes, and competitor actions
- Automatically adjust bids, budgets, and targeting
- Test ad creatives and scale winners
- Reallocate budget to high-performing campaigns
- Provide actionable insights and recommendations

Use your reasoning capabilities to:
- Understand business goals and constraints
- Analyze multi-dimensional performance data
- Make data-driven optimization decisions
- Adapt to market volatility and platform changes
- Balance short-term performance with long-term strategy
- Explain your decisions clearly to business owners

Always prioritize ROI, cost-efficiency, and sustainable growth. Think strategically before taking action.`,
      idleSessionTtlInSeconds: 3600, // Increased timeout for better stability
      description: 'AI Advertisement Optimization Agent for Small Businesses - Using Claude 3.5 Sonnet v2',
    });

    // Action Group for Google Ads
    const googleAdsActionGroup = new bedrock.CfnAgentActionGroup(this, 'GoogleAdsActionGroup', {
      agentId: agent.attrAgentId,
      agentVersion: 'DRAFT',
      actionGroupName: 'google-ads-actions',
      actionGroupExecutor: {
        lambda: googleAdsFunction.functionArn,
      },
      apiSchema: {
        payload: JSON.stringify({
          openapi: '3.0.0',
          info: {
            title: 'Google Ads Management API',
            version: '1.0.0',
            description: 'Manage Google Ads campaigns, get metrics, adjust bids and budgets',
          },
          paths: {
            '/campaigns': {
              get: {
                summary: 'Get list of Google Ads campaigns',
                description: 'Retrieve all active Google Ads campaigns',
                operationId: 'getGoogleCampaigns',
                responses: {
                  '200': {
                    description: 'List of campaigns',
                    content: {
                      'application/json': {
                        schema: {
                          type: 'object',
                          properties: {
                            campaigns: {
                              type: 'array',
                              items: {
                                type: 'object',
                                properties: {
                                  id: { type: 'string' },
                                  name: { type: 'string' },
                                  status: { type: 'string' },
                                  budget: { type: 'number' },
                                },
                              },
                            },
                          },
                        },
                      },
                    },
                  },
                },
              },
            },
            '/metrics': {
              get: {
                summary: 'Get campaign performance metrics',
                description: 'Retrieve performance metrics for a specific campaign',
                operationId: 'getGoogleMetrics',
                parameters: [
                  {
                    name: 'campaignId',
                    in: 'query',
                    required: true,
                    schema: { type: 'string' },
                    description: 'Campaign ID',
                  },
                ],
                responses: {
                  '200': {
                    description: 'Campaign metrics',
                  },
                },
              },
            },
            '/adjust-bid': {
              post: {
                summary: 'Adjust campaign bid',
                description: 'Adjust bid for a campaign by percentage',
                operationId: 'adjustGoogleBid',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          bidAdjustment: { type: 'number', description: 'Percentage adjustment (e.g., 10 for +10%, -15 for -15%)' },
                        },
                        required: ['campaignId', 'bidAdjustment'],
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Bid adjusted successfully' },
                },
              },
            },
            '/update-budget': {
              post: {
                summary: 'Update campaign budget',
                description: 'Update daily budget for a campaign',
                operationId: 'updateGoogleBudget',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          newBudget: { type: 'number', description: 'New daily budget in dollars' },
                        },
                        required: ['campaignId', 'newBudget'],
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Budget updated successfully' },
                },
              },
            },
            '/toggle-status': {
              post: {
                summary: 'Pause or activate campaign',
                description: 'Change campaign status to PAUSED or ENABLED',
                operationId: 'toggleGoogleStatus',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          status: { type: 'string', enum: ['PAUSED', 'ENABLED'] },
                        },
                        required: ['campaignId', 'status'],
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Status changed successfully' },
                },
              },
            },
          },
        }),
      },
    });

    // Action Group for Meta Ads
    const metaAdsActionGroup = new bedrock.CfnAgentActionGroup(this, 'MetaAdsActionGroup', {
      agentId: agent.attrAgentId,
      agentVersion: 'DRAFT',
      actionGroupName: 'meta-ads-actions',
      actionGroupExecutor: {
        lambda: metaAdsFunction.functionArn,
      },
      apiSchema: {
        payload: JSON.stringify({
          openapi: '3.0.0',
          info: {
            title: 'Meta Ads Management API',
            version: '1.0.0',
            description: 'Manage Meta (Facebook/Instagram) Ads campaigns',
          },
          paths: {
            '/campaigns': {
              get: {
                summary: 'Get list of Meta Ads campaigns',
                operationId: 'getMetaCampaigns',
                responses: {
                  '200': { description: 'List of campaigns' },
                },
              },
            },
            '/metrics': {
              get: {
                summary: 'Get campaign performance metrics',
                operationId: 'getMetaMetrics',
                parameters: [
                  {
                    name: 'campaignId',
                    in: 'query',
                    required: true,
                    schema: { type: 'string' },
                  },
                ],
                responses: {
                  '200': { description: 'Campaign metrics' },
                },
              },
            },
            '/adjust-bid': {
              post: {
                summary: 'Adjust campaign bid',
                operationId: 'adjustMetaBid',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          bidAdjustment: { type: 'number' },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Bid adjusted' },
                },
              },
            },
            '/update-budget': {
              post: {
                summary: 'Update campaign budget',
                operationId: 'updateMetaBudget',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          newBudget: { type: 'number' },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Budget updated' },
                },
              },
            },
            '/toggle-status': {
              post: {
                summary: 'Pause or activate campaign',
                operationId: 'toggleMetaStatus',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          status: { type: 'string', enum: ['PAUSED', 'ACTIVE'] },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Status changed' },
                },
              },
            },
            '/test-creative': {
              post: {
                summary: 'Test creative variants',
                operationId: 'testMetaCreative',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignId: { type: 'string' },
                          creativeVariants: { type: 'array' },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'A/B test started' },
                },
              },
            },
          },
        }),
      },
    });

    // Action Group for Analytics
    const analyticsActionGroup = new bedrock.CfnAgentActionGroup(this, 'AnalyticsActionGroup', {
      agentId: agent.attrAgentId,
      agentVersion: 'DRAFT',
      actionGroupName: 'analytics-actions',
      actionGroupExecutor: {
        lambda: analyticsFunction.functionArn,
      },
      apiSchema: {
        payload: JSON.stringify({
          openapi: '3.0.0',
          info: {
            title: 'Performance Analytics API',
            version: '1.0.0',
            description: 'Analyze campaign performance and generate insights',
          },
          paths: {
            '/analyze-performance': {
              get: {
                summary: 'Analyze campaign performance',
                operationId: 'analyzePerformance',
                parameters: [
                  {
                    name: 'campaignId',
                    in: 'query',
                    required: true,
                    schema: { type: 'string' },
                  },
                  {
                    name: 'days',
                    in: 'query',
                    required: false,
                    schema: { type: 'integer', default: 7 },
                  },
                ],
                responses: {
                  '200': { description: 'Performance analysis' },
                },
              },
            },
            '/detect-trends': {
              get: {
                summary: 'Detect performance trends',
                operationId: 'detectTrends',
                parameters: [
                  {
                    name: 'campaignId',
                    in: 'query',
                    required: true,
                    schema: { type: 'string' },
                  },
                ],
                responses: {
                  '200': { description: 'Detected trends' },
                },
              },
            },
            '/compare-campaigns': {
              post: {
                summary: 'Compare multiple campaigns',
                operationId: 'compareCampaigns',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          campaignIds: { type: 'array', items: { type: 'string' } },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Campaign comparison' },
                },
              },
            },
            '/recommendations': {
              get: {
                summary: 'Get optimization recommendations',
                operationId: 'getRecommendations',
                parameters: [
                  {
                    name: 'campaignId',
                    in: 'query',
                    required: true,
                    schema: { type: 'string' },
                  },
                ],
                responses: {
                  '200': { description: 'Recommendations' },
                },
              },
            },
            '/cross-platform': {
              get: {
                summary: 'Analyze cross-platform performance',
                operationId: 'crossPlatformAnalysis',
                responses: {
                  '200': { description: 'Cross-platform analysis' },
                },
              },
            },
          },
        }),
      },
    });

    // Action Group for Budget Optimizer
    const budgetOptimizerActionGroup = new bedrock.CfnAgentActionGroup(this, 'BudgetOptimizerActionGroup', {
      agentId: agent.attrAgentId,
      agentVersion: 'DRAFT',
      actionGroupName: 'budget-optimizer-actions',
      actionGroupExecutor: {
        lambda: budgetOptimizerFunction.functionArn,
      },
      apiSchema: {
        payload: JSON.stringify({
          openapi: '3.0.0',
          info: {
            title: 'Budget Optimization API',
            version: '1.0.0',
            description: 'Optimize budget allocation across campaigns',
          },
          paths: {
            '/optimize': {
              post: {
                summary: 'Optimize budget allocation',
                operationId: 'optimizeBudget',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          totalBudget: { type: 'number' },
                          campaignIds: { type: 'array', items: { type: 'string' } },
                          goal: { type: 'string', enum: ['maximize_roas', 'minimize_cpa', 'maximize_conversions'] },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Optimized allocation' },
                },
              },
            },
            '/reallocate': {
              post: {
                summary: 'Reallocate budget between campaigns',
                operationId: 'reallocateBudget',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          fromCampaign: { type: 'string' },
                          toCampaign: { type: 'string' },
                          amount: { type: 'number' },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Budget reallocated' },
                },
              },
            },
            '/recommendations': {
              get: {
                summary: 'Get budget recommendations',
                operationId: 'getBudgetRecommendations',
                parameters: [
                  {
                    name: 'totalBudget',
                    in: 'query',
                    required: true,
                    schema: { type: 'number' },
                  },
                ],
                responses: {
                  '200': { description: 'Budget recommendations' },
                },
              },
            },
            '/simulate': {
              post: {
                summary: 'Simulate budget scenarios',
                operationId: 'simulateScenarios',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          scenarios: { type: 'array' },
                        },
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Simulation results' },
                },
              },
            },
          },
        }),
      },
    });

    // Action Group for Storage
    const storageActionGroup = new bedrock.CfnAgentActionGroup(this, 'StorageActionGroup', {
      agentId: agent.attrAgentId,
      agentVersion: 'DRAFT',
      actionGroupName: 'storage-actions',
      actionGroupExecutor: {
        lambda: storageFunction.functionArn,
      },
      apiSchema: {
        payload: JSON.stringify({
          openapi: '3.0.0',
          info: {
            title: 'Campaign Insights Storage API',
            version: '1.0.0',
            description: 'Store and retrieve campaign insights and decisions',
          },
          paths: {
            '/store': {
              post: {
                summary: 'Store campaign insight',
                operationId: 'storeInsight',
                requestBody: {
                  required: true,
                  content: {
                    'application/json': {
                      schema: {
                        type: 'object',
                        properties: {
                          key: { type: 'string', description: 'Unique identifier for the insight' },
                          data: { type: 'string', description: 'Insight data to store' },
                        },
                        required: ['key', 'data'],
                      },
                    },
                  },
                },
                responses: {
                  '200': { description: 'Insight stored successfully' },
                },
              },
            },
            '/retrieve': {
              get: {
                summary: 'Retrieve campaign insight',
                operationId: 'retrieveInsight',
                parameters: [
                  {
                    name: 'key',
                    in: 'query',
                    required: true,
                    schema: { type: 'string' },
                    description: 'Unique identifier for the insight',
                  },
                ],
                responses: {
                  '200': { description: 'Retrieved insight data' },
                },
              },
            },
          },
        }),
      },
    });

    // Outputs
    new cdk.CfnOutput(this, 'AgentId', {
      value: agent.attrAgentId,
      description: 'Bedrock Agent ID',
    });

    new cdk.CfnOutput(this, 'CampaignDataBucketName', {
      value: campaignDataBucket.bucketName,
      description: 'S3 Bucket for campaign data storage',
    });

    new cdk.CfnOutput(this, 'MetricsTableName', {
      value: metricsTable.tableName,
      description: 'DynamoDB table for campaign metrics',
    });

    new cdk.CfnOutput(this, 'APIKeysSecretArn', {
      value: apiKeysSecret.secretArn,
      description: 'Secrets Manager ARN for API keys',
    });
  }
}
