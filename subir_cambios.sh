#!/bin/bash

# Planner Pro - One Click Deploy Script
# Usage: ./deploy.sh "Optional Commit Message"

echo "🚀 Starting Deployment Process..."

# 1. Initialize Git if missing
if [ ! -d ".git" ]; then
    echo "📦 Initializing Repository..."
    git init
    # NOTE: User must set remote manually once. Script will prompt if missing.
    git branch -M main
fi

# 2. Check Remote
REMOTE=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE" ]; then
    echo "⚠️  No remote configuration found!"
    echo "Please run this command once to connect your GitHub:"
    echo "git remote add origin https://github.com/samuelhes/plannerprogenerator.git"
    echo ""
    echo "Then run ./deploy.sh (or ./subir_cambios.sh) again."
    exit 1
fi

# 3. Add Changes
echo "📝 Adding files..."
git add .

# 4. Commit using argument or default timestamp
MSG="$1"
if [ -z "$MSG" ]; then
    MSG="Auto-Deploy $(date '+%Y-%m-%d %H:%M:%S')"
fi
echo "💾 Committing: $MSG"
git commit -m "$MSG"

# 5. Push
echo "☁️  Pushing to GitHub (which triggers Render)..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Success! Deployment started on Render."
    echo "Visit: https://dashboard.render.com/ to see progress."
else
    echo "❌ Push failed."
    echo "If this is your first time, you might need to sign in."
    echo "Try running: 'git push -u origin main' manually to authenticate."
fi
