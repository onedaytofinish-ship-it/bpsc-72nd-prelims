# Plan — Complete BLOCK 1 & BLOCK 2 (Topics 9–23)

> Created 2026-07-17 00:50 IST • Anchor: exam 26 Jul 2026 • CA window: Jan 2025 → 15 Jul 2026 (emphasis Jan–Jul 2026)

## Scope
- **Block 1 remainder (Current Affairs, wt 1.7):** topics 9 awards, 10 sports, 11 reports/indices, 12 days/themes, 13 books/obituaries, 14 environment
- **Block 2 (Bihar Current Affairs, wt 1.3):** topics 15 schemes, 16 budget, 17 appointments, 18 awards, 19 sports, 20 infra, 21 surveys/data, 22 festivals/culture, 23 Bihar in national reports
- Topics 1–8 already done → 15 topics remain. All Lane R (need live research).

## Stage 1 — Research cache (6 parallel coder workers → `research/*.md`)
| Worker | Cache file | Feeds topics |
|:--|:--|:--|
| R1 | research/ca_awards_2025_26.md | 9, 18 |
| R2 | research/ca_sports_2025_26.md | 10, 19 |
| R3 | research/ca_reports_indices_2025_26.md | 11, 23 |
| R4 | research/ca_days_books_env_2025_26.md | 12, 13, 14 |
| R5 | research/ca_bihar_schemes_budget_2025_26.md | 15, 16, 21 |
| R6 | research/ca_bihar_govt_infra_culture_2025_26.md | 17, 20, 22 |

Citation rule: every dated fact/number traces to a cached source (URL + retrieval date).

## Stage 2 — Writers (15 parallel coder workers, one per topic)
Each reads: `briefs/writer_contract.md` (output contract), `Topics/8_science_and_tech_in_news.html` (template exemplar), its research cache file(s), its PYQ excerpts from `BPSC PYQ/pyq_mappings.json`.
Outputs per topic: `Topics/{NN}_{slug}.html` (8 sections, 25 MCQs, v2.2 house template) + `Topics/mcq/{NN}_{slug}.json` (v3 sidecar) + optional 1 subpage + ≥2 local images.

## Stage 3 — QA + Answer audit (gate)
1. `python3 qa_check.py 9..23` — structural checks on HTML + validates MCQ JSON sidecars. Must pass 15/15.
2. 15 parallel explore auditors re-solve every MCQ from the JSON sidecars independently; report mismatches.
3. Coder fix workers repair any mismatch (HTML answers key + explanation + JSON must agree). 100% pass required.

## Stage 4 — Integration (orchestrator)
- Flip cards 9–23 locked→active in `Topics/index.html`; update stats (done 8→23, coverage %).
- Set `topics_master.json` status done for 9–23.
- Append 15 rows to `worklog.md`; update statistics.
- Report coverage: Σwt(1–23) = 8×1.7 done before… recompute in worklog (23 topics ≈ 13.6+11.7 = 25.3+... compute exactly).
