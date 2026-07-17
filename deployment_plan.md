# Deployment Plan — Netlify + GitHub

## Overview
Deploy the BPSC 72nd Prelims study site (static HTML/CSS/JS in `Topics/`) to Netlify via GitHub automatic deploys.

**Current state:** No git repo exists. Project is 669MB but only ~74MB is deployable web content.
**Target:** `https://bpsc-72nd-prelims.netlify.app` (or similar), auto-deploying on every `git push` to `main`.

---

## Step 1: Create `.gitignore`

Exclude large/unnecessary folders to keep the repo under GitHub's recommended limits.

**Exclude:**
- `Resources/` — 549MB of PDFs/source material (not needed for the website)
- `BPSC PYQ/` — 46MB of OCR cache + PYQ PDFs (reference only, not deployed)
- `.DS_Store` — macOS noise
- `__pycache__/` / `*.pyc` — Python cache
- `.vscode/` — editor config (optional, can include)

**Include:**
- `Topics/` — the website (74MB: HTML + images + MCQ JSON + subpages + _assets)
- `topics_master.json` — tracking file
- `qa_check.py` — QA tool
- `worklog.md` — build log
- `plan.md`, `implementation_plan.md` — project docs
- `research/` — research notes (288KB, small)
- `briefs/` — writing briefs (8KB, small)

---

## Step 2: Initialize Git Repo & Push to GitHub

```bash
# 1. Initialize git
cd /Users/cray/Desktop/BPSC_Topics_kimi
git init
git add .
git commit -m "Initial commit: BPSC 72nd Prelims study site (35/158 topics)"

# 2. Create GitHub repo (via github.com or `gh` CLI)
gh repo create bpsc-72nd-prelims --public --source=. --remote=origin
# OR manually create on github.com, then:
git remote add origin git@github.com:cray238/bpsc-72nd-prelims.git

# 3. Push
git branch -M main
git push -u origin main
```

**Expected repo size:** ~75MB (Topics/ 74MB + small files). Well within GitHub's limits.

---

## Step 3: Configure Netlify

### Option A: via Netlify UI (recommended for first time)
1. Go to **https://app.netlify.com** → "Add new site" → "Import from Git"
2. Connect your GitHub account → select `bpsc-72nd-prelims` repo
3. Configure:
   - **Build command:** *(none — static site, no build step)*
   - **Publish directory:** `Topics`
   - **Branch:** `main`
4. Click "Deploy site"

### Option B: via `netlify.toml` (recommended for reproducibility)
Create a `netlify.toml` in the project root:

```toml
[build]
  publish = "Topics"
  # No build command — static HTML site

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"

# Redirect root to Topics/index.html
[[redirects]]
  from = "/"
  to = "/index.html"
  status = 200
```

Then push to GitHub → Netlify auto-detects and deploys.

---

## Step 4: Verify Deployment

1. **Netlify URL:** Netlify assigns a random URL like `https://bpsc-72nd-prelims.netlify.app`
2. **Verify:**
   - `index.html` loads (Master Dashboard with 35 topic cards)
   - Click a topic card (e.g., Topic 35) → loads the topic page
   - Images load (Bhagat Singh, Bose, etc.)
   - MCQ quiz works (radio buttons, check answers, score display)
   - Navbar appears (auto-injected by `navbar.js`)
   - Subpage links work (e.g., "Master Detail →")
3. **Custom domain** (optional): Settings → Domain management → add custom domain

---

## Step 5: Auto-Deploy Workflow (Ongoing)

Once set up, every `git push` to `main` triggers a Netlify rebuild:

```bash
# After building a new topic (e.g., Topic 36):
git add .
git commit -m "Add Topic 36 (Constitutional Acts)"
git push
# Netlify auto-deploys in ~30 seconds
```

**Preview deploys:** Netlify also creates preview deploys for pull requests — useful for QA before merging.

---

## File Size Considerations

| Folder | Size | Include in Repo? | Reason |
|--------|------|-------------------|--------|
| `Topics/` | 74MB | ✅ Yes | The website — this is what Netlify deploys |
| `Topics/images/` | 70MB | ✅ Yes | Images served by the website |
| `Resources/` | 549MB | ❌ No | PDFs/source material — too large, not needed for web |
| `BPSC PYQ/` | 46MB | ❌ No | OCR cache + PYQ PDFs — reference only |
| `research/` | 288KB | ✅ Yes | Small, useful for reference |
| `briefs/` | 8KB | ✅ Yes | Small, useful for reference |
| `.DS_Store` | ~varies | ❌ No | macOS noise |

**Repo total:** ~75MB — well within GitHub's 1GB recommended limit.

---

## Security Notes

- **No secrets:** The project contains no API keys, passwords, or sensitive data — all content is public study material
- **Public repo:** Safe to make public (all content is educational material for BPSC exam prep)
- **Netlify free tier:** 100GB bandwidth/month, unlimited sites — more than sufficient for a study site

---

## Quick Start (Copy-Paste Commands)

```bash
# 1. Create .gitignore
cd /Users/cray/Desktop/BPSC_Topics_kimi

cat > .gitignore << 'EOF'
Resources/
BPSC PYQ/
.DS_Store
__pycache__/
*.pyc
.vscode/
EOF

# 2. Initialize git
git init
git add .
git commit -m "Initial commit: BPSC 72nd Prelims study site (35/158 topics)"

# 3. Create GitHub repo & push
gh repo create bpsc-72nd-prelims --public --source=. --remote=origin --push
# OR manually create on github.com and:
# git remote add origin git@github.com:YOUR_USERNAME/bpsc-72nd-prelims.git
# git branch -M main
# git push -u origin main

# 4. Go to https://app.netlify.com → Import from Git → select repo
#    - Publish directory: Topics
#    - No build command
#    - Deploy!
```