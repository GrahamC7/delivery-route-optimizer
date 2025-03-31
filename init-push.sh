#!/bin/bash

# First-time Git setup and push script
# Usage: bash init-push.sh

echo "✅ Initializing Git repository..."
git init

echo "📦 Adding all files..."
git add .

echo "✍️ Making first commit..."
git commit -m "feat: initial commit with project setup"

# Ask for your GitHub repo URL
read -p "🔗 Enter your GitHub repo URL: " repo_url

echo "🔧 Setting remote origin..."
git remote add origin "$repo_url"

echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "🎉 Done! Your code is live on GitHub."
