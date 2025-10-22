# AWS Amplify Hosting Setup

## 🌐 Host Your Demo Online

### 1. Create Amplify App
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify project
amplify init

# Add hosting
amplify add hosting
# Choose: Amazon CloudFront and S3
# Choose: DEV (S3 only with HTTP)

# Deploy
amplify publish
```

### 2. Your Online Demo URL
After deployment, you'll get a URL like:
```
https://main.d1234567890.amplifyapp.com/web-demo.html
```

### 3. Custom Domain (Optional)
```bash
# Add custom domain
amplify add hosting
# Choose: Amazon CloudFront and S3
# Enter your domain: ai-ad-optimizer.yourdomain.com
```

## 📱 Mobile-Friendly Demo

Update web-demo.html for better mobile experience:
- Responsive design ✅ (already included)
- Touch-friendly buttons ✅
- Mobile viewport ✅
- Fast loading ✅

## 🎯 For Competition Judges

### Online Access Points
1. **Demo Website**: https://your-amplify-url.com/web-demo.html
2. **GitHub Repository**: https://github.com/username/ai-ad-optimizer-agent
3. **AWS Console**: Provide temporary access credentials
4. **Video Demo**: Upload to YouTube/Vimeo

### What Judges Can Do Online
- ✅ View project documentation
- ✅ See architecture diagrams
- ✅ Access AWS Console (with credentials)
- ✅ Watch video demonstrations
- ✅ Review complete source code
- ✅ See deployment instructions