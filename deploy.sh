#!/bin/bash
# Deploy script: push to GitHub + deploy to Netlify
# Usage: ./deploy.sh "commit message"

cd /Users/cray/Desktop/BPSC_Topics_kimi

MSG="${1:-Update BPSC study site}"

echo "=== Committing changes ==="
git add .
git commit -m "$MSG"

echo "=== Pushing to GitHub ==="
git push origin main

echo "=== Deploying to Netlify ==="
netlify deploy --prod --dir=Topics

echo "=== Done! ==="
echo "Site: https://bpsc-72nd-prelims.netlify.app"
echo "Repo: https://github.com/onedaytofinish-ship-it/bpsc-72nd-prelims"