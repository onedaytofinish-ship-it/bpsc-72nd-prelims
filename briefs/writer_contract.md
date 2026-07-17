# Writer Contract — BPSC 72nd Prelims Topic Pages (v2.2 house template + v3 MCQ sidecar)

You are generating ONE exam-study topic page for the BPSC 72nd Prelims (exam: 26 Jul 2026, 150 MCQs, ⅓ negative). The student has ~9 days. Output = marks: fact-dense, Bihar-first, PYQ-anchored, BPSC-level MCQs.

## Required reading (in this order)
1. **Template exemplar:** `/Users/cray/Desktop/BPSC_Topics_kimi/Topics/8_science_and_tech_in_news.html` — mirror its structure, inline CSS, section order, MCQ HTML/JS pattern EXACTLY (classes, ids, `const answers = {...}`, checkAnswers() logic, score display).
2. **Your research cache file(s)** — assigned in your mission. Every dated fact/number (2025–2026) MUST come from the cache or a source you personally re-verify via web search. NO invented numbers. If the cache lacks something you need, do 1–3 targeted web searches and cite the source URL in the Reference Links section.
3. **Your PYQ excerpts:** key = your slug (e.g. `9_awards_and_honours`) in `/Users/cray/Desktop/BPSC_Topics_kimi/BPSC PYQ/pyq_mappings.json`. Extract with:
   `python3 -c "import json;d=json.load(open('/Users/cray/Desktop/BPSC_Topics_kimi/BPSC PYQ/pyq_mappings.json'));import sys;[print(x['source'],'p'+str(x['page']),'|',x['text'][:300],'\n---') for x in d['YOUR_KEY']]"`
   The OCR is noisy — mine it for question THEMES and fact types, then build PYQ-inspired MCQs and PYQ boxes around those themes.

## Output files
1. `/Users/cray/Desktop/BPSC_Topics_kimi/Topics/{NN}_{slug}.html`
2. `/Users/cray/Desktop/BPSC_Topics_kimi/Topics/mcq/{NN}_{slug}.json` — array of EXACTLY the same 25 MCQs as in the HTML:
   ```json
   [{"q":"...","options":["...","...","...","..."],"answer":2,"explanation":"...","difficulty":"pyq|bpsc|tricky","pyq_ref":"71st p.12 | null"}]
   ```
   `answer` is 0-based (0=A … 3=D).
3. Optional: ONE subpage `Topics/subpages/{NN}_..._detail.html` (core concepts + statics + background + current relevance), linked from the main page.
4. ≥2 relevant images saved into `Topics/images/` (download from Wikimedia Commons via curl; e.g. `curl -L -o Topics/images/foo.jpg 'URL'`). Reference as `<img src="images/foo.jpg" ...>`. Verify the file exists and is non-tiny (>10 KB) after download; if download fails, use another source. Never hotlink.

## HTML content requirements — 8 sections (same semantics as exemplar)
1. **Topic Header** — number, Tier A, weight (1.7 for topics 9–14; 1.3 for 15–23), expected questions. `<title>{NN} - {Topic Name} | BPSC 72nd Prelims</title>`. Back-link to index.html at top (copy exemplar).
2. **Core Content** — bullet-dense, tables for ≥3 comparable items, ≥2 PYQ boxes ("PYQ Alert" style like exemplar) quoting the theme of real past questions.
3. **Fact Matrix** — high-density quick-revision table(s).
4. **Bihar Connection 🔗** — MANDATORY, substantive (state-specific facts/data, not filler).
5. **Cross-Topic Connections** — reference other topic numbers (see `topics_master.json` list; e.g. awards→topic 60 static awards, sports→62, reports→7/11, Bihar topics→geography 88–96 etc.).
6. **Current Relevance 2024–26** — latest developments from cache, with dates.
7. **MCQ Practice Set — 25 Questions (BPSC Level)** — pattern MUST match exemplar exactly:
   - `<div class="mcq-block" id="qN">` (N=1..25 sequential), radio inputs `name="qN"` value a/b/c/d
   - `<div class="mcq-explanation" id="expN">` containing the marker `Correct Answer: (X)` (capital letter)
   - one `<script>` block: `const answers = {q1: 'a', ..., q25: 'd'};` (lowercase) + checkAnswers() copied from exemplar
   - score display `id="scoreNum">0/25<` and section header `MCQ Practice Set — 25 Questions`
   - Mix: 40% PYQ-inspired (difficulty "pyq"), 40% probable BPSC-level ("bpsc"), 20% tricky traps ("tricky"). Include multi-statement (1,2,3 which-correct) and matching-style questions like real BPSC. Explanations must say WHY the right option is right AND why the trap option is wrong.
8. **Reference Links** — 5–10 curated URLs (official/govt/reputed; for Lane R these should match cache sources).

## Style
- Copy the exemplar's `<style>` block and adapt minimally (dark header #1a1a2e, accent #e94560, Bihar-orange #ff6b35, Inter/system fonts, print-friendly page breaks).
- Concise: 8–15 printed pages equivalent. Bullets > paragraphs. Mnemonics for hard lists (≥1 mnemonic box).
- NO placeholder text (TODO/TBD/XXX/Lorem/FIXME forbidden).

## Self-QA before returning
Run: `python3 /Users/cray/Desktop/BPSC_Topics_kimi/qa_check.py {NN}` — it must print PASS. Fix until it passes.

## Return (≤10 lines)
Files written | MCQ count | images saved | subpage (if any) | any facts you flagged as uncertain (with why).
