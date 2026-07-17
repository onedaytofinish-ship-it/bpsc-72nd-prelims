# BPSC 72nd Prelims — Topic Generation System v2 (Efficient, Output-Oriented)

> **Plan date:** 2026-07-16 (21:15 IST) • **Exam:** Sunday 2026-07-26, 12:00–14:00, offline OMR
> **Updated:** 2026-07-18 — Status: 62/158 topics done (39.2%), quality audit completed
> Supersedes v1 (archived at `implementation_plan_v1_archive.md`).

---

## 1. Ground Truth (verified this session)

| Fact | Value | Source |
|:--|:--|:--|
| Exam date & shift | 26 July 2026, 12:00–14:00, single shift | BPSC exam calendar / adda247 / PW (Jul 2026) |
| Pattern | 150 MCQs × 1 mark, 2 hrs, **⅓ negative**, qualifying-only | BPSC notification |
| Vacancies | 1,186 (revised from 1,230) | PW / adda247 |
| 71st cut-off (UR Male) | **88/150** (⅓ negative introduced in 71st) | BPSC result Nov 2025 |
| 71st good attempts | 110–130 Qs; accuracy was decisive | Exam analyses |
| 71st CA flavour | "More Bihar-specific than national" | Plutus IAS analysis |
| **Score target** | **≥100 net** (≈115–125 accurate attempts) | Cut-off + 10-mark buffer |

**Priority currency:** the tracker (`72nd Prelims Tracker.htm`) assigns every topic a weight
(`wt`) = its expected question count. Σwt = 150.8 ≈ the whole paper. **All prioritization,
coverage metrics, and cut lines in this plan use `wt`.** Canonical topic list: `topics_master.json`
(extracted from the tracker; numbering 1–158 is authoritative — note it differs from v1 after #23).

---

## 2. Why v1 Was Inefficient (diagnosis)

| # | v1 Problem | Cost |
|:--|:--|:--|
| D1 | Serial generation (~27 min/topic) | 153 remaining ≈ 69 hrs > time available |
| D2 | Live web research for *every* topic | Wasted on 135 static topics that never change |
| D3 | Template drift (v1.0→v2.3 in one day) | Retrofit debt on Topics 1–2; inconsistent output |
| D4 | Hand-maintained `index.html` + worklog | Bookkeeping time per topic; drifts out of sync |
| D5 | MCQs trapped inside HTML | Can't rebuild into mock tests; can't audit answer keys |
| D6 | No triage line — 158 topics treated uniformly | Low-yield topics (wt 0.4) compete with wt 1.7 topics |
| D7 | Manual quality checklist | Doesn't scale; answer-key errors slip through |
| D8 | Open questions never resolved | Maths format, CA window, PDF pipeline all ambiguous |

## 3. v2 Operating Principles

1. **Output = marks.** Every artifact must either cover expected questions (`wt`) or improve accuracy (practice/audit). If it does neither, don't build it.
2. **Two-lane production.** Static knowledge needs no web research; only Current Affairs does.
3. **Parallel batches.** 4 subagents per batch, each with a complete brief — the main agent never hand-writes topic bodies, only briefs, verifies, and integrates.
4. **Frozen template.** v3.0 is final. Change requests go to a parking lot, reviewed only on Day 8.
5. **Scripted verification.** If a check can be scripted, it must not be done by eye.
6. **Cut from the bottom.** Behind schedule → drop lowest-`wt` topics first. Never drop Tier A.

---

## 4. Production Lanes

### Lane R — Research Lane (Current Affairs): Topics 6–23 (18 remaining)
- **Needs:** live web research, 2025→July 2026 window, Bihar-specific angle per 71st trend.
- **Shared research cache:** one deep search per *cluster* feeds many topics. Cache notes in `research/` (markdown, with source URLs + retrieval date) before briefing subagents:
  - `research/ca_national_2025_26.md` → feeds 6,7,8,9,10,11,12,13,14
  - `research/ca_bihar_2025_26.md` → feeds 15–23
  - `research/schemes_2025_26.md`, `research/reports_indices_2026.md` → feed 1,11,15,23
- **Citation rule:** every dated fact/number in a Lane R topic must trace to a cached source. No uncited numbers.

### Lane K — Knowledge Lane (Static): Topics 24–149, 155–158 (≈135 topics)
- **Needs:** no web research. Model knowledge + `BPSC PYQ/pyq_mappings.json` excerpts are sufficient.
- Subagents receive: topic brief from `topics_master.json`, the topic's mapped PYQ questions, template spec, output contract.
- Optional: 1–2 spot-check searches only where facts may have changed (e.g., "current Chief Justice" in polity topics — resolve via Lane R cache instead).

### Lane M — Maths Lane: Topics 50–59 (10 topics)
- **Output-oriented decision (resolves v1 open question):** Maths needs practice, not reading.
  Lighter template: formula table + 10 worked examples + **30 practice MCQs** (10 easy / 15 BPSC-level / 5 tricky). No subpages, no images, no Bihar-connection box beyond one line.

---

## 5. Template v3.0-FINAL (frozen)

**Asset extraction:** shared `Topics/_assets/topic.css` + `Topics/_assets/topic.js` created once.
Per-topic HTML references them → per-file size drops ~40%, visual consistency guaranteed,
regeneration cheap.

**8 sections (unchanged semantics from v2.3):**
1. Topic Header (number, tier, wt, expected Qs) 2. Core Content + PYQ boxes
3. Fact Matrix tables 4. Bihar Connection (mandatory) 5. Cross-Topic links
6. Current Relevance 2024–26 7. Interactive MCQ set 8. Reference links

**MCQ sidecar (new, mandatory):** every topic also writes `Topics/mcq/NN_name.json`:
```json
[{"q": "...", "options": ["...","...","...","..."], "answer": 2,
  "explanation": "...", "difficulty": "bpsc", "pyq_ref": "70th p.12 | null"}]
```
This single change unlocks: automated answer-key audits, unlimited recombined mock tests,
per-topic drill sets, and an error-log revision tool.

**Counts:** 25 MCQs per standard topic (30 for Lane M). Difficulty mix: 40% PYQ-inspired /
40% probable / 20% tricky — matching BPSC's multi-statement and matching styles.

**Retrofit policy:** no patching. Topics 1–2 get **regenerated** in v3 on Day 7 (content already
researched; regeneration is cheaper and cleaner than retrofit).

---

## 6. Pipeline & Automation

```
topics_master.json ──┐
pyq_mappings.json ───┼─► Batch Brief (main agent) ─► 4 parallel subagents
research/*.md ───────┘        (template + brief + PYQs + research notes)
                                        │
                            HTML + mcq/NN.json per topic
                                        │
              qa_check.py (structure, MCQ JSON valid, answer∈options,
                           images exist, internal links resolve)
                                        │
              answer_audit (independent solver subagent re-solves
                            every MCQ from JSON; mismatches fixed)
                                        │
              build_index.py ─► index.html + worklog row (auto, no hand edits)
```

**Scripts to build tonight (Day 0):**
| Script | Function |
|:--|:--|
| `qa_check.py` | Per-topic structural verification; fails the batch loudly |
| `answer_audit` workflow | Solver subagent prompt + JSON compare; 100% pass required before "Done" |
| `build_index.py` | Regenerates dashboard from filesystem + `topics_master.json` (status, coverage %) |
| `build_mock.py` | Assembles N-question mocks from `mcq/*.json` with answer sheet |

**Throughput model:** batch of 4 ≈ 25–35 min wall time (parallel) → **8–10 topics/hr** for
Lane K; Lane R ≈ 4–6/hr (research-bound). Remaining work ≈ 18–22 hrs of generation across
6 production days — feasible; v1's serial model was not.

---

## 7. Schedule & Coverage Gates (anchored to 2026-07-16 IST)

| Day | Date | Production | Cumulative coverage (Σwt / 150.8) |
|:--|:--|:--|:--|
| 0 | Wed 16 Jul (tonight) | Freeze v3 template + `_assets`; build 4 scripts; build Lane R research cache | 8.5 (5.6%) |
| 1 | Thu 17 Jul | Lane R: topics 6–14 (national CA) | +15.3 |
| 2 | Fri 18 Jul | Lane R: topics 15–23 (Bihar CA) • **Gate 1** | **35.5 (24%)** |
| 3 | Sat 19 Jul | Lane K: Modern History 24–37 (14) | +12.6 |
| 4 | Sun 20 Jul | Lane K: Polity 38–49 (12) + Lane M start 50–54 • **Gate 2** | **≈59 (39%)** |
| 5 | Mon 21 Jul | Lane M: 55–59 + Static GK 60–68 (14) | +14 |
| 6 | Tue 22 Jul | Lane K: Biology 69–77 (9) + Economy 78–87 (10) • **Gate 3** | **≈90 (60%)** |
| 7 | Wed 23 Jul | Lane K: Bihar Geo 88–96 (9) + Bihar Polity/Economy 143–149 (7); regenerate Topics 1–2 in v3; full answer-audit sweep | **≈104 (69%)** |
| 8 | Thu 24 Jul | Tier B by wt: Chem 107–114, Physics 115–122, Indian Geo 123–130, then 97–106 / 131–142 / 150–158 **only if Gates 1–3 met**. Build 3 full mocks + Revision Pack | up to ≈135–150 |
| 9 | Fri 25 Jul | **No new content.** 2 timed mocks, Revision Pack, error-log review, exam logistics | — |
| 10 | Sat 26 Jul | **EXAM 12:00–14:00.** Morning: Fact Matrices + mnemonics only | — |

**Cut lines (activate the moment a gate is missed — drop in this order):**
1. Environment 150–154 (wt 0.4) → 2. Bihar History 155–158 (0.5) → 3. Medieval 137–142 + Ancient 97–106 (0.7) → 4. World Geo 131–136 + Economy remainder (0.8) → 5. Chem/Physics/Indian Geo (0.9, keep highest-PYQ first).
Never cut: topics 1–96 Tier A, Bihar-tagged topics (27, 32, 34, 100–102, 104, 142, 155–157).

**Study-side deliverables (the "output" in output-oriented):**
- **Revision Pack** (Day 8): single printable HTML of every topic's Fact Matrix + PYQ boxes + mnemonics. → PDF via headless Chrome (verified installed).
- **3 full-length mocks** (Day 8) from MCQ sidecars, weighted to PYQ subject distribution (CA ~31, Hist ~28, Sci ~25, Geo ~19, Bihar ~16, Polity ~13, Quant ~10, Econ ~7).
- **Error log** (Day 9): user's wrong answers from mocks mapped back to topic files.

---

## 8. Open Questions — Resolved

| v1 Question | Decision |
|:--|:--|
| Skip Maths topics? | **No — convert to Lane M** (formula sheet + worked examples + 30 MCQs). Quant is 10 free marks if formulas are memorized. |
| CA date focus? | **Jan 2025 → 15 Jul 2026**, emphasis Jan–Jul 2026; Bihar CA gets equal depth (71st was Bihar-heavy). |
| PDF pipeline? | **HTML-first.** Only the Day-8 Revision Pack + mocks get batch PDF (headless Chrome — confirmed available alongside weasyprint/pandoc). No per-topic PDFs. |

---

## 9. Metrics (tracked in auto-worklog)

| Metric | Target |
|:--|:--|
| Coverage % = Σwt(Done) / 150.8 | ≥69% by Day 7, ≥85% by Day 8 |
| MCQ bank size | 25 × topics done (30 × Lane M) |
| Answer-audit pass rate | 100% before any topic marked Done |
| Uncited facts in Lane R topics | 0 |
| Gate adherence | Missed gate ⇒ same-day cut-line activation |

## 10. Risk Controls

| Risk | Control |
|:--|:--|
| Wrong MCQ answer keys (highest-severity) | Independent solver audit on 100% of MCQs from JSON before Done |
| CA hallucination | Research-cache citation rule; subagent may only use cached/retrieved facts |
| Time overrun | Gates + pre-agreed cut lines (§7); no "just one more topic" |
| Template churn | v3 frozen; change parking lot reviewed Day 8 only |
| Parallel inconsistency | Single `_assets` CSS/JS + strict output contract in every brief |
| Burnout / diminishing returns | Day 9 is practice-only; coverage beyond Gate 3 is explicitly optional |

---

*Next action: Day 0 build — v3 template assets, `qa_check.py`, `build_index.py`, `build_mock.py`, and Lane R research cache.*

---

## 11. Quality Standards Audit (Added 2026-07-18)

### Audit Findings — Blocks 7 (Biology), 10 (Ancient History), 15 (Medieval History)

**Issue 1 — Image Relevance (FIXED 2026-07-18):**
- 17 of 20 files had mismatched images (e.g., Bhimbetka rock art in cell biology topic, Mahabodhi Temple in Delhi Sultanate topic, Mahabodhi Temple in Sher Shah Suri topic)
- Downloaded 24 new topically-relevant images from Wikimedia Commons
- Updated all 20 HTML files with correct images matching their topics
- All files re-verified with `qa_check.py` — 20/20 PASS

**Issue 2 — Content Length & Depth (MONITORING):**
- Block 10/15 average ~580 lines vs exemplar Topic 8 at 1220 lines
- Tier B topics (wt 0.7) — some brevity acceptable, but content density should be improved
- New topics 73-77 generated at ~620-690 lines with fact-dense tables

**Issue 3 — Block 7 Completeness (FIXED 2026-07-18):**
- 5 missing topics (73-77) generated — all Tier A, wt 1.0
- All 5 pass `qa_check.py` with MCQ sidecar JSON + subpages

### Quality Standards for All Future Topics (Mandatory)

1. **Image Relevance Rule:** Every image MUST be directly relevant to the topic. No recycling images from unrelated topics. If a relevant image is not available, download one from Wikimedia Commons using `Special:FilePath` approach.

2. **Minimum Content Standards:**
   - Tier A topics: ≥600 lines, ≥3 tables, ≥2 images, ≥1 mnemonic, ≥1 PYQ box, ≥25 MCQs
   - Tier B topics: ≥550 lines, ≥2 tables, ≥2 images, ≥1 mnemonic, ≥1 exam tip box, ≥25 MCQs
   - Lane M (Maths): ≥400 lines, formula table, 10 worked examples, 30 MCQs

3. **MCQ Quality Standards:**
   - 25 MCQs per standard topic (30 for Lane M)
   - Difficulty mix: 40% PYQ-inspired / 40% probable / 20% tricky
   - Every explanation MUST explain WHY the correct answer is right AND WHY trap options are wrong
   - Answer keys must be shuffled (never all 'A') — use `shuffle_answers_v2.py`
   - MCQ sidecar JSON mandatory: `Topics/mcq/NN_slug.json`
   - MCQs must be hardcoded in HTML (not fetched from JSON) for offline use

4. **Bihar Connection Standards:**
   - Tier A: ≥5 Bihar-specific points with specific data (numbers, institutions, programmes)
   - Tier B: ≥4 Bihar-specific points
   - Bihar-tagged topics (27, 32, 34, 100-102, 104, 142, 155-157): ≥6 Bihar points

5. **Structural Requirements:**
   - 8 sections: Header, Core Content+PYQ box, Fact Matrix, Bihar Connection, Cross-Topic, Current Relevance, MCQ Practice Set, References
   - Subpage mandatory: `Topics/subpages/NN_slug_detail.html`
   - Prediction box (72nd BPSC top 5-7 predictions) between Current Relevance and MCQ section
   - Navbar CSS/JS link in all pages
   - Print-friendly CSS

6. **Verification Pipeline (no topic marked Done until ALL pass):**
   - `python3 qa_check.py NN` — structural verification
   - Answer audit — solver re-solves every MCQ from JSON; 100% match
   - No placeholder text (TODO/TBD/XXX/Lorem/FIXME)
   - No broken internal links
   - All images exist and are topically relevant

### Revised Schedule (2026-07-18, Day 3)

| Day | Date | Production | Status |
|:--|:--|:--|:--|
| 0-2 | 16-18 Jul | Lane R (1-23) + image audit + Block 7/10/15 | ✅ DONE (62/158) |
| 3 | 18 Jul | Polity 38-49 + Lane M 50-54 | In progress |
| 4 | 19 Jul | Lane M 55-59 + Static GK 60-68 | — |
| 5 | 20 Jul | Economy 78-87 + Chem 107-114 | — |
| 6 | 21 Jul | Physics 115-122 + Indian Geo 123-130 | — |
| 7 | 22 Jul | Bihar Geo 88-96 + Bihar Polity 143-149; regen 1-2 in v3 | — |
| 8 | 23 Jul | Tier B remainder + World Geo 131-136 + mocks + revision pack | — |
| 9 | 24 Jul | Practice only: 2 timed mocks, revision, error log | — |
| 10 | 25 Jul | EXAM (note: exam is 26 Jul per latest info) | — |
