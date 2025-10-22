#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AIAgentStack } from '../lib/ai-agent-stack-simplified';

const app = new cdk.App();
new AIAgentStack(app, 'AdOptimizerAgentStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1',
  },
  description: 'AI Advertisement Optimization Agent for Small Businesses',
});
