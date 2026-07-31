# BPSC 72nd Prelims — Implementation Plan v3 (Post-Postponement)

> **Plan date:** 2026-07-31 • **Exam: POSTPONED, new date not yet announced**
> **Progress at plan time:** 62/158 topics, Σwt 68.3 / 150.8 = **45.3% coverage**
> Supersedes `implementation_plan.md` (v2). v2 archived as the record of Days 0–2.

---

## 1. What changed

| | v2 assumption | v3 reality |
|:--|:--|:--|
| Exam date | Sun 26 Jul 2026, fixed | **Postponed 18 Jul 2026 by BPSC notice. New date TBA.** |
| Time budget | 10 days, hard stop | Unknown, but ≥6 weeks likely (BPSC historically re-schedules 6–10 weeks out) |
| Governing constraint | Calendar | **Coverage, not calendar** |
| Cut lines | Active — drop Tier C to fit | **Suspended.** With the reprieve, 100% coverage is reachable |
| Cadence | Parallel batches of 4 | **One topic at a time**, reviewed before the next starts |

The v2 schedule (Day 0–10) is void. v3 replaces dates with an **ordered queue + coverage
checkpoints**. Nothing in the queue is time-boxed; the queue is worked top-down until the
exam date is announced, at which point §6 re-plans against real days remaining.

**Unchanged:** the v3.0-FINAL template, the 8-section structure, the MCQ sidecar contract,
the quality standards in v2 §11, and the `wt` priority currency. Those are frozen.

---

## 2. Current state (verified 2026-07-31)

**Done — 62 topics, Σwt 68.3**

| Group | Topics | Σwt |
|:--|:--|--:|
| Current Affairs | 1–14 | 23.8 |
| Bihar Current Affairs | 15–23 | 11.7 |
| Modern Indian History | 24–37 | 12.6 |
| Biology | 69–77 | 9.0 |
| Ancient History | 97–106 | 7.0 |
| Medieval History | 137–142 | 4.2 |

**Assets:** 62 topic pages · 54 MCQ sidecars · 67 subpages · 111 images · shared `_assets/`
**Repo:** clean at `a8534a4` (18 Jul), `worklog.md` uncommitted
**Deploy:** static, publish dir `Topics/`; Netlify + Cloudflare Pages both configured

---

## 3. Production queue (work top-down)

Ordered by **marginal yield** = weight gained per unit of effort. Research-free Tier A
topics with the highest per-topic `wt` come first; the cheap consolidation tier comes last.

| Phase | Topics | # | Σwt | Lane | Cumulative coverage |
|:--|:--|--:|--:|:--|--:|
| — | *(current)* | — | — | — | 68.3 — **45.3%** |
| **P1** | Static GK 60–68 | 9 | 9.0 | K | 77.3 — **51.3%** |
| **P2** | Maths & Reasoning 50–59 | 10 | 10.0 | M | 87.3 — **57.9%** |
| **P3** | Indian Polity 38–49 | 12 | 10.8 | K | 98.1 — **65.1%** |
| **P4** | Bihar Geography 88–96 | 9 | 8.1 | K | 106.2 — **70.4%** |
| **P5** | Indian Economy 78–87 | 10 | 8.0 | K+ | 114.2 — **75.7%** |
| **P6** | Bihar Polity 143–145 · Bihar Economy 146–149 | 7 | 6.2 | K+ | 120.4 — **79.8%** |
| **P7** | Chemistry 107–114 · Physics 115–122 · Indian Geography 123–130 | 24 | 21.6 | K | 142.0 — **94.2%** |
| **P8** | World Geography 131–136 | 6 | 4.8 | K | 146.8 — **97.3%** |
| **P9** | Bihar History 155–158 · Environment 150–154 | 9 | 4.0 | C | 150.8 — **100%** |

*Lane K = static knowledge, no web research. Lane M = maths (lighter template, 30 MCQs).
Lane K+ = static plus 1–2 spot-checks for figures that move (repo rate, budget numbers).
Lane C = consolidation, see §3.4.*

### 3.1 Why Static GK is first, not Polity
Nine topics at `wt 1.0` each — the highest per-topic weight of anything remaining, tied
only with Maths. Zero research. Highly PYQ-repetitive (BPSC recycles awards/firsts/
superlatives/HQ questions almost verbatim). Fastest weight-per-hour on the board.

### 3.2 Why Maths is second
Ten guaranteed marks that depend on formula recall, not reading. Lane M's lighter
template (formula table + 10 worked examples + 30 practice MCQs, no subpage, no images)
makes these the cheapest pages in the project to build. Reasoning (58, 59) is pure
pattern practice — MCQ volume matters more than prose.

### 3.3 Why Bihar Geography moved up (was Day 7 in v2)
The 71st paper was assessed as "more Bihar-specific than national." Bihar Geography is
9 Tier A topics at `wt 0.9` that v2 had scheduled behind Chemistry and Physics. That was
a mis-ranking. It moves ahead of Economy.

### 3.4 Phase 9 is consolidation, not new content
Bihar History 155–158 and Environment 150–154 substantially restate material already
written:

| Pending topic | Already covered in |
|:--|:--|
| 155 Ancient Bihar | 100 Mahajanapadas, 101 Buddhism/Jainism, 102 Mauryan, 104 Gupta |
| 156 Medieval Bihar | 142 Sher Shah Suri (Sasaram) |
| 157 Modern Bihar | 27 Revolt 1857 (Kunwar Singh), 32 Gandhian (Champaran), 34 Quit India |
| 158 Cultural heritage | 22 Bihar festivals & culture |
| 150 Ecosystem / 151 Biodiversity | 77 Biotech & ecology |
| 152 Climate change / 154 Conventions | 14 Environment in news |
| 153 Pollution | 14 Environment in news |

Build these as **revision-and-drill pages**: condensed fact matrix + cross-links to the
source topics + a fresh 25-MCQ set. Do not re-research. Nine topics, ~4.0 wt, at maybe a
third the normal cost.

---

## 4. Per-topic loop (one at a time)

Each topic is a complete unit. Nothing moves to the next until every step passes.

```
1. BRIEF     topics_master.json entry + pyq_mappings.json hits for the topic
             + Bihar-angle requirement + (Lane K+/R only) research cache excerpt
2. GENERATE  Topics/NN_slug.html          — 8 sections, v3.0-FINAL template
             Topics/mcq/NN_slug.json      — 25 MCQs (30 for Lane M)
             Topics/subpages/NN_slug_detail.html   (skipped for Lane M)
3. VERIFY    python3 qa_check.py NN       — structure, div balance, MCQ count,
                                            images exist, internal links resolve
4. AUDIT     independent re-solve of every MCQ from the JSON; 100% match required
             python3 shuffle_answers_v2.py — no answer-key clustering
5. INTEGRATE index.html card locked→active · topics_master.json status→done
             · worklog.md row
6. COMMIT    one topic per commit, message "Topic NN: <title> — <n> MCQs, QA PASS"
7. REVIEW    hand back before starting NN+1
```

**Quality bar per v2 §11 (unchanged):** Tier A ≥600 lines / ≥3 tables / ≥2 topically
relevant images / ≥1 mnemonic / ≥1 PYQ box / ≥5 Bihar points. Tier B ≥550 lines / ≥4
Bihar points. No image recycled from an unrelated topic. Every MCQ explanation says why
the key is right *and* why each trap is wrong.

---

## 5. Debt backlog (interleaved, non-blocking)

Worked between phases, not before them. D1 first — it unblocks the mock tests.

| # | Item | Why it matters | Cost |
|:--|:--|:--|:--|
| **D1** | **MCQ sidecars for topics 1–8** — extract the 8 topics' MCQs from their HTML into `mcq/NN.json`. Extract, don't regenerate. | These 8 are invisible to the answer audit and excluded from every mock test. Largest single hole in the bank. | Small |
| **D2** | `build_index.py` — regenerate `index.html` from filesystem + `topics_master.json` | v2 diagnosed hand-maintained index as problem D4 and never fixed it. Index has drifted twice already. | Small |
| **D3** | `build_mock.py` — assemble weighted N-question mocks from `mcq/*.json` + answer sheet | The whole point of the sidecar contract. Blocked on D1 for full coverage but usable now at 54 topics. | Small |
| **D4** | Full answer-audit sweep across all existing sidecars | Audits were per-topic at write time; no sweep since. Wrong keys are the highest-severity defect in the project. | Medium |
| **D5** | Regenerate topics 1–2 to v3.0 template | v1.0 template, visibly inconsistent with the rest of the site. Cosmetic, not marks. | Medium |
| **D6** | **CA refresh, topics 1–23** | **Gated — see §6.** | Large |

---

## 6. The current-affairs problem

Topics 1–23 (Σwt 35.5 — the heaviest block in the paper) were researched to a **15 Jul 2026
cutoff** against a 26 Jul exam. Every month the exam slips, that block decays: new
appointments, new summits, new index editions, new Bihar schemes.

**Rule: do not refresh CA until the new date is public.** A refresh done now would have to
be redone. Refreshing twice costs double and risks introducing errors on facts that were
already correct.

**Trigger:** BPSC announces the new date → immediately re-plan:
1. Set the CA research window to **Jan 2025 → (exam date − 10 days)**.
2. Rebuild `research/*.md` cache for the extended window (6 cluster searches).
3. Refresh topics 1–23 against the new cache — figures, appointments, rankings, Bihar CA.
4. Re-run the answer audit on all 23 (rankings changing invalidates keys silently).

**Watch:** set a recurring check on `bpsc.bihar.gov.in` notices so the trigger isn't missed.

---

## 7. Coverage checkpoints (replace v2's date gates)

| Checkpoint | At | Action |
|:--|:--|:--|
| **C1** | End of P2 — 57.9% | D1 + D3 done → build **Mock #1** (150 Qs, PYQ-weighted). Take it timed. Start the error log. |
| **C2** | End of P5 — 75.7% | **Mock #2**. Error log review — any topic scoring <60% gets a targeted drill set, not a rewrite. |
| **C3** | End of P7 — 94.2% | **Mock #3**. D4 full answer-audit sweep. |
| **C4** | End of P9 — 100% | **Revision Pack**: single printable HTML of every Fact Matrix + PYQ box + mnemonic → PDF via headless Chrome. |
| **C5** | Exam date announced | Trigger §6. Re-plan remaining queue against real days. Cut lines return only if days-remaining < topics-remaining ÷ 3. |

Mock weighting follows the PYQ subject distribution: CA ~31, History ~28, Science ~25,
Geography ~19, Bihar ~16, Polity ~13, Quant ~10, Economy ~7.

---

## 8. Metrics

| Metric | Target |
|:--|:--|
| Coverage Σwt(done) / 150.8 | 100% before exam date |
| MCQ bank | 25 × topics done (30 × Lane M) → ~4,000 at completion |
| Answer-audit pass rate | 100% before any topic marked done |
| Topics with sidecar | 158/158 (currently 54/62) |
| Mock score trajectory | Mock #1 baseline → ≥100/150 net by Mock #3 |
| Uncited facts in CA topics | 0 |

---

## 9. Risks

| Risk | Control |
|:--|:--|
| **Exam announced with short notice** | Queue is ordered by yield, so stopping anywhere leaves the highest-value work done. C5 re-plan reinstates cut lines. |
| **CA block decays further** | §6 gating; single refresh pass triggered by the announcement. |
| **Wrong answer keys** (highest severity) | Per-topic audit at write time + D4 sweep at C3. |
| **Momentum loss during an open-ended wait** | Coverage checkpoints give fixed milestones independent of the calendar; mocks at C1/C2/C3 keep it practice-driven. |
| **Index/tracker drift** | D2 makes it generated, not hand-edited. |
| **Quality drift at one-topic cadence** | Per-topic review step (loop step 7) before the next starts. |

---

## 10. Immediate next actions

1. Commit the pending `worklog.md`.
2. **D1** — extract MCQ sidecars for topics 1–8.
3. **P1** — begin Topic 60 (Awards, static), one topic at a time.
4. Set up a recurring check for the BPSC exam-date notice.
