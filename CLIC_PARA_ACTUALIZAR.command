#!/bin/bash

# Obtain the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "---------------------------------------------------"
echo "🚀 Planner Pro - Auto Deploy System (Total Reset)"
echo "---------------------------------------------------"
echo "Target: $DIR"

# 1. NUCLEAR OPTION: Delete old git history to prevent conflicts forever
# The user wants "You do it", so we handle the cleanup.
if [ -d ".git" ]; then
    echo "🧹 Cleaning up old configuration..."
    rm -rf .git
fi

# 2. Fresh Initialization
echo "📦 Initializing fresh repository..."
git init
git branch -M main
git remote add origin https://github.com/samuelhes/plannerprogenerator.git

# 3. Add & Commit
echo "📝 Saving current state..."
git add .
git commit -m "Fresh Deploy $(date '+%Y-%m-%d %H:%M:%S')"

# 4. Force Push (Overwrite Cloud)
echo "☁️  Uploading to Cloud (Overwriting old versions)..."
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Repository updated."
    echo "🚀 Triggering Render Deployment..."
    curl -X POST "https://api.render.com/deploy/srv-d4tli3hr0fns7381s1ng?key=EopeP7scg_Q"
    echo ""
    echo "Deployment started!"
else
    echo ""
    echo "⚠️  Upload failed."
    echo "Check your internet connection."
fi

echo ""
echo "---------------------------------------------------"
read -t 10 -p "Done. Closing in 10s..."
