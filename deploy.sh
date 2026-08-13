#!/bin/bash
# Deploy script: push to GitHub + deploy to Netlify
# Usage: ./deploy.sh "commit message"
#
# GitHub:  onedaytofinish-ship-it/bpsc-72nd-prelims (push via gh CLI token)
# Netlify: 72prelimsbpsc235238 (site ID: 4c5f8703-f7c5-4af0-8d79-d9ad94183d12)
# Netlify account: onedaytofinish2@gmail.com (team: One day)

cd /Users/cray/Desktop/BPSC_Topics_kimi

MSG="${1:-Update BPSC study site}"

echo "=== Committing changes ==="
git add .
git commit -m "$MSG"

echo "=== Pushing to GitHub (onedaytofinish-ship-it) ==="
GH_TOKEN=$(gh auth token --user onedaytofinish-ship-it 2>/dev/null)
if [ -z "$GH_TOKEN" ]; then
  echo "ERROR: gh CLI not authenticated as onedaytofinish-ship-it"
  echo "Run: gh auth switch --user onedaytofinish-ship-it"
  exit 1
fi
git push https://onedaytofinish-ship-it:${GH_TOKEN}@github.com/onedaytofinish-ship-it/bpsc-72nd-prelims.git main

echo "=== Deploying to Netlify ==="
netlify deploy --prod --dir=Topics

echo "=== Done! ==="
echo "Site: https://72prelimsbpsc235238.netlify.app"
echo "Repo: https://github.com/onedaytofinish-ship-it/bpsc-72nd-prelims"