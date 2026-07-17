#!/usr/bin/env python3
"""QA checker for Topic 7 economy page (same checks as house standard)."""
import re, sys, os

BASE = "/Users/cray/Desktop/BPSC_Topics_kimi/Topics"
PAGE = os.path.join(BASE, "7_economy_in_news.html")

html = open(PAGE, encoding="utf-8").read()
errors = []

# 1. Count mcq-block divs, answers keys, explanation divs
mcq_ids = re.findall(r'<div class="mcq-block" id="q(\d+)">', html)
ans_block = re.search(r'const answers = \{(.*?)\};', html, re.S)
answers = dict(re.findall(r"q(\d+): '([abcd])'", ans_block.group(1))) if ans_block else {}
exp_ids = re.findall(r'<div class="mcq-explanation" id="exp(\d+)">', html)

n_mcq, n_ans, n_exp = len(mcq_ids), len(answers), len(exp_ids)
if not (n_mcq == n_ans == n_exp):
    errors.append(f"COUNT MISMATCH: mcq-block={n_mcq}, answers={n_ans}, explanations={n_exp}")

# 2. Sequential ids
def check_seq(ids, label):
    nums = sorted(int(i) for i in ids)
    if nums != list(range(1, len(nums) + 1)):
        errors.append(f"{label} ids not sequential: {nums}")
check_seq(mcq_ids, "mcq-block")
check_seq(exp_ids, "explanation")

# 3. Every explanation letter matches its answers key
expl_pairs = re.findall(
    r'<div class="mcq-explanation" id="exp(\d+)">.*?Correct Answer: \(([A-D])\)', html, re.S)
seen = set()
for num, letter in expl_pairs:
    seen.add(num)
    key = answers.get(num)
    if key is None:
        errors.append(f"exp{num}: no answers key")
    elif key.upper() != letter:
        errors.append(f"exp{num}: explanation says ({letter}) but answers key is '{key}'")
if len(seen) != n_exp:
    errors.append(f"Only {len(seen)} of {n_exp} explanations contain a 'Correct Answer: (X)' marker")

# 4. Score display equals N
m = re.search(r'id="scoreNum">0/(\d+)<', html)
if not m:
    errors.append("scoreNum display not found")
elif int(m.group(1)) != n_ans:
    errors.append(f"score display shows 0/{m.group(1)} but answers count is {n_ans}")

# 5. Section header states the count
hm = re.search(r'MCQ Practice Set — (\d+) Questions', html)
if not hm:
    errors.append("MCQ header count not found")
elif int(hm.group(1)) != n_ans:
    errors.append(f"MCQ header says {hm.group(1)} questions but there are {n_ans}")

# 6. Every referenced image file exists
imgs = re.findall(r'<img src="([^"]+)"', html)
for src in imgs:
    p = os.path.join(BASE, src)
    if not os.path.isfile(p):
        errors.append(f"image missing: {src}")
if not imgs:
    errors.append("no <img> tags found")

# 7. No placeholder text
for pat in [r'TODO', r'PLACEHOLDER', r'XXX', r'TBD', r'Lorem ipsum', r'FIXME']:
    if re.search(pat, html, re.I):
        errors.append(f"placeholder text found: {pat}")

# 8. Subpage link target exists
for href in re.findall(r'href="(subpages/[^"]+)"', html):
    if not os.path.isfile(os.path.join(BASE, href)):
        errors.append(f"subpage link missing: {href}")

# 9. All qN names in options match an mcq block id
radio_names = set(re.findall(r'name="q(\d+)"', html))
if radio_names != set(mcq_ids):
    errors.append("radio names don't match mcq-block ids")

print(f"mcq-blocks={n_mcq} answers={n_ans} explanations={n_exp} score-display=0/{m.group(1) if m else '?'} images={len(imgs)}")
if errors:
    print("FAIL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS")
