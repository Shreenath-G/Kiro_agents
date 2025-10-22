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
      timeout: cdk.Duration.seconds(60),
      memorySize: 512,
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
      timeout: cdk.Duration.seconds(60),
      memorySize: 512,
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
      timeout: cdk.Duration.seconds(60),
      memorySize: 512,
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

    // Create Bedrock Agent with Nova model
    const agent = new bedrock.CfnAgent(this, 'AdOptimizerAgent', {
      agentName: 'ad-optimizer-agent',
      agentResourceRoleArn: agentRole.roleArn,
      foundationModel: 'amazon.nova-pro-v1:0',
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
      idleSessionTtlInSeconds: 1800,
      description: 'AI Advertisement Optimization Agent for Small Businesses',
    });

    // NOTE: Action Groups must be added manually in AWS Console after deployment
    // CDK does not yet support CfnAgentActionGroup in version 2.220.0

    // Outputs
    new cdk.CfnOutput(this, 'AgentId', {
      value: agent.attrAgentId,
      description: 'Bedrock Agent ID - Use this to add action groups in AWS Console',
    });

    new cdk.CfnOutput(this, 'AgentArn', {
      value: agent.attrAgentArn,
      description: 'Bedrock Agent ARN',
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

    new cdk.CfnOutput(this, 'GoogleAdsFunctionArn', {
      value: googleAdsFunction.functionArn,
      description: 'Google Ads Lambda Function ARN',
    });

    new cdk.CfnOutput(this, 'MetaAdsFunctionArn', {
      value: metaAdsFunction.functionArn,
      description: 'Meta Ads Lambda Function ARN',
    });

    new cdk.CfnOutput(this, 'AnalyticsFunctionArn', {
      value: analyticsFunction.functionArn,
      description: 'Analytics Lambda Function ARN',
    });

    new cdk.CfnOutput(this, 'BudgetOptimizerFunctionArn', {
      value: budgetOptimizerFunction.functionArn,
      description: 'Budget Optimizer Lambda Function ARN',
    });

    new cdk.CfnOutput(this, 'StorageFunctionArn', {
      value: storageFunction.functionArn,
      description: 'Storage Lambda Function ARN',
    });

    new cdk.CfnOutput(this, 'NextSteps', {
      value: 'After deployment, add action groups in AWS Console: https://console.aws.amazon.com/bedrock/home#/agents',
      description: 'Manual steps required',
    });
  }
}
