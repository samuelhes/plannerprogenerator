#!/bin/bash

# Configuration
REPO_URL="https://github.com/samuelhes/plannerprogenerator.git"
COMMIT_MSG="🚀 Desktop Fix v2.6.3 (Tags UI + Version) $(date +'%Y-%m-%d %H:%M:%S')"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}===============================================${NC}"
echo -e "${YELLOW}   PLANNER PRO GENERATOR - DEPLOYMENT SCRIPT   ${NC}"
echo -e "${YELLOW}===============================================${NC}"

# Navigate to script directory
cd "$(dirname "$0")"

echo -e "\n${GREEN}[1/5] Initializing Git repository...${NC}"
# Remove existing git if any to ensure clean slate
rm -rf .git
git init
git branch -m main

echo -e "\n${GREEN}[2/5] Configuring credentials...${NC}"
# Use local config to avoid global side effects
git config user.name "Planner Pro Deployer"
git config user.email "deploy@plannerpro.com"

echo -e "\n${GREEN}[3/5] Adding files...${NC}"
git add .

echo -e "\n${GREEN}[4/5] Committing changes...${NC}"
git commit -m "$COMMIT_MSG"

echo -e "\n${GREEN}[5/5] Pushing to GitHub (Force)...${NC}"
git remote add origin "$REPO_URL"
git push -f origin main

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ SUCCESS! Deployment triggered.${NC}"
    echo -e "Monitor progress at: https://dashboard.render.com/"
else
    echo -e "\n${RED}❌ ERROR: Push failed.${NC}"
    echo -e "Please check your internet connection and GitHub permissions."
fi

echo -e "\n${YELLOW}Press any key to exit...${NC}"
read -n 1 -s
