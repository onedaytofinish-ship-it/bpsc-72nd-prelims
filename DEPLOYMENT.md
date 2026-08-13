# BPSC 72nd Prelims — Deployment Configuration
# ═══════════════════════════════════════════════════════════════
#
# GitHub: onedaytofinish-ship-it/bpsc-72nd-prelims
# Netlify site ID: 91f9602e-2c24-4c5b-aea3-e7f34e385af8
# Site URL: https://bpsc-72nd-prelims.netlify.app
#
# PROBLEM: macOS keychain has 'preptez001' credentials stored, which
# does NOT have push access to onedaytofinish-ship-it/bpsc-72nd-prelims.
# Need to update keychain or use a different auth method.
#
# ═══════════════════════════════════════════════════════════════
# HOW TO FIX (run these commands in the terminal manually):
# ═══════════════════════════════════════════════════════════════

# ── STEP 1: Remove old GitHub credentials from keychain ─────────
# This removes the preptez001 token that's blocking pushes:
#
#   security delete-internet-password -s github.com
#
# ── STEP 2: Add onedaytofinish-ship-it credentials ───────────────
# Option A: Personal Access Token (PAT) — RECOMMENDED
#   1. Go to https://github.com/settings/tokens (as onedaytofinish-ship-it)
#   2. Generate a classic token with 'repo' scope
#   3. Run: git credential approve <<< "protocol=https
# host=github.com
# username=onedaytofinish-ship-it
# password=ghp_YOUR_TOKEN_HERE
# "
#
# Option B: Switch to SSH
#   git remote set-url origin git@github.com:onedaytofinish-ship-it/bpsc-72nd-prelims.git
#   (requires SSH key to be added to onedaytofinish-ship-it's GitHub account)
#
# ── STEP 3: Push to GitHub ──────────────────────────────────────
#   git push origin main
#
# ── STEP 4: Re-authenticate Netlify ─────────────────────────────
#   netlify login
#   (authorize in browser)
#
# ── STEP 5: Deploy to Netlify ───────────────────────────────────
#   netlify deploy --prod --dir=Topics
#
# ═══════════════════════════════════════════════════════════════
# ALTERNATIVE: Deploy with Netlify auth token (no login needed)
# ═══════════════════════════════════════════════════════════════
# If you have a Netlify personal access token:
#
#   NETLIFY_AUTH_TOKEN=nfp_YOUR_TOKEN netlify deploy --prod --dir=Topics --site 91f9602e-2c24-4c5b-aea3-e7f34e385af8
#
# ═══════════════════════════════════════════════════════════════
# CURRENT STATUS (2026-08-13) — DEPLOYED SUCCESSFULLY
# ═══════════════════════════════════════════════════════════════
# - Git commit: ✅ committed (104c017)
# - GitHub push: ✅ pushed to onedaytofinish-ship-it/bpsc-72nd-prelims
#   (used gh CLI token, NOT preptez001 keychain credentials)
# - Netlify deploy: ✅ deployed to https://72prelimsbpsc235238.netlify.app
#   (site: 72prelimsbpsc235238, ID: 4c5f8703-f7c5-4af0-8d79-d9ad94183d12)
#   (account: onedaytofinish2@gmail.com, team: One day)
#
# NOTE: The old Netlify site (bpscprelims721146, ID: 91f9602e...) belongs
# to a different Netlify account and is no longer accessible. The new
# active site is 72prelimsbpsc235238.
#
# DEPLOY COMMANDS (for future deploys):
#   ./deploy.sh "commit message"  # commits + pushes + deploys in one go
#   # Or manual:
#   git push https://onedaytofinish-ship-it:$(gh auth token --user onedaytofinish-ship-it)@github.com/onedaytofinish-ship-it/bpsc-72nd-prelims.git main
#   netlify deploy --prod --dir=Topics