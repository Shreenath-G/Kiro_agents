@echo off
echo Creating public GitHub repository for AI Advertisement Optimization Agent
echo.

echo Step 1: Initialize Git repository
git init

echo Step 2: Add all files
git add .

echo Step 3: Create initial commit
git commit -m "Initial commit: AI Advertisement Optimization Agent - Competition Submission"

echo Step 4: Connect to GitHub (replace YOUR_USERNAME with your GitHub username)
echo git remote add origin https://github.com/YOUR_USERNAME/ai-ad-optimizer-agent.git
echo git branch -M main
echo git push -u origin main

echo.
echo IMPORTANT: Replace YOUR_USERNAME with your actual GitHub username in the commands above
echo Then run those three commands to upload your code
echo.
echo Your public repository will be available at:
echo https://github.com/YOUR_USERNAME/ai-ad-optimizer-agent
echo.
pause