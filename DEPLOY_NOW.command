#!/bin/bash

# One-Click Deploy Script
# Double-click this file to upload your code to GitHub!

# 1. Navigate to the folder where this script (and your code) is located
cd "$(dirname "$0")"

# Hardcoded Target Request by User
TARGET_REPO="https://github.com/samuelhes/plannerprogenerator.git"

# Color Codes for pretty output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   AUTO-DEPLOY TO GITHUB & RENDER 🚀   ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# 2. Check for Git
if [ ! -d ".git" ]; then
    echo "Initializing new Git repository..."
    git init
    git branch -M main
else
    echo "Git repository already active."
fi

# 3. Add & Commit
echo -e "${GREEN}Preparing files...${NC}"
git add .
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Auto-deploy update: $TIMESTAMP" || echo "Nothing new to commit."

# 4. Check/Set Remote Connection
EXISTING_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [ "$EXISTING_REMOTE" != "$TARGET_REPO" ]; then
    echo -e "${GREEN}Configuring GitHub Repository...${NC}"
    # Remove old origin if it exists but is wrong
    if [ -n "$EXISTING_REMOTE" ]; then
        git remote remove origin
    fi
    git remote add origin "$TARGET_REPO"
    echo "Connected to: $TARGET_REPO"
fi

# 5. Push!
echo ""
echo -e "${GREEN}Uploading to GitHub...${NC}"
echo "Pushing to $TARGET_REPO..."
git push -u origin main

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   SUCCESS! CODE UPLOADED. ✅          ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo "Render should now detect the change automatically."
echo "Press any key to close..."
read -n 1 -s
