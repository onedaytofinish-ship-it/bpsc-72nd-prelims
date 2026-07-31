#!/usr/bin/env python3
"""QA checker for BPSC topic pages. Usage: python3 qa_check.py 9 10 11 ... | python3 qa_check.py all
Checks HTML structure (mcq blocks, answer keys, explanations, score display, images,
subpage links, placeholders) AND validates the MCQ JSON sidecar in Topics/mcq/."""
import re, sys, os, json, glob

BASE = "/Users/cray/Desktop/BPSC_Topics_kimi/Topics"


# --- page/sidecar answer-agreement check (added 2026-07-31) ------------------
# qa_check used to verify only HTML-internal consistency, which stayed green while
# shuffle_answers_v2 desynced 97 answer keys. This is the check that catches it.
import unicodedata as _ud
_MARK = re.compile(r'^\s*(?:\(([A-D])\)|([A-D])[.)])\s+')

def _plain(s):
    s = re.sub(r'<br\s*/?>', ' ', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    import html as _h
    return re.sub(r'\s+', ' ', _h.unescape(s).replace('\xa0', ' ')).strip()

def _strip_marker(s, idx=None):
    m = _MARK.match(s)
    if not m:
        return s.strip()
    if idx is not None and (m.group(1) or m.group(2)) != "ABCD"[idx]:
        return s.strip()
    return s[m.end():].strip()

def _norm(s, idx=None):
    return re.sub(r'[^a-z0-9]', '', _strip_marker(_ud.normalize('NFKD', str(s)), idx).lower())

def check_page_sidecar_agreement(html, questions):
    """Return a list of error strings where the page's keyed option text differs
    from the sidecar's keyed option text."""
    errs = []
    km = re.search(r'const answers\s*=\s*\{(.*?)\};', html, re.S)
    if not km or not questions:
        return errs
    keys = {int(a): l for a, l in re.findall(r"q(\d+)\s*:\s*'([abcd])'", km.group(1))}
    for i, q in enumerate(questions, 1):
        blk = re.search(r'<div class="mcq-block" id="q%d">(.*?)(?=<div class="mcq-block" id="q\d+">'
                        r'|<div class="answer-key|</body>)' % i, html, re.S)
        if not blk or i not in keys:
            continue
        raw = re.findall(r'<label class="mcq-option">.*?value="([abcd])"\s*>(.*?)</label>', blk.group(1), re.S)
        opts = q.get("options") or []
        ans = q.get("answer")
        if len(raw) != 4 or len(opts) != 4 or not isinstance(ans, int):
            continue
        page = {v: _norm(_plain(t), "abcd".index(v)) for v, t in raw}
        side = [_norm(o, k) for k, o in enumerate(opts)]
        if sorted(page.values()) != sorted(side):
            continue          # wording differs between page and sidecar; not comparable
        if page[keys[i]] != side[ans]:
            errs.append(f"PAGE/SIDECAR KEY DISAGREE q{i}: page marks ({keys[i].upper()}), "
                        f"sidecar marks ({'ABCD'[ans]}) — different option text")
    return errs
# ---------------------------------------------------------------------------

def check_topic(num):
    pages = glob.glob(os.path.join(BASE, f"{num}_*.html"))
    pages = [p for p in pages if not os.path.basename(p).startswith("index")]
    if not pages:
        return num, None, [f"no HTML file matching {num}_*.html"]
    page = pages[0]
    slug = os.path.basename(page)[:-5]
    html = open(page, encoding="utf-8").read()
    errors = []

    # 1. mcq blocks / answers / explanations counts
    mcq_ids = re.findall(r'<div class="mcq-block" id="q(\d+)">', html)
    ans_block = re.search(r'const answers = \{(.*?)\};', html, re.S)
    answers = dict(re.findall(r"q(\d+): '([abcd])'", ans_block.group(1))) if ans_block else {}
    exp_ids = re.findall(r'<div class="mcq-explanation" id="exp(\d+)">', html)
    n_mcq, n_ans, n_exp = len(mcq_ids), len(answers), len(exp_ids)
    if not (n_mcq == n_ans == n_exp):
        errors.append(f"COUNT MISMATCH: mcq-block={n_mcq}, answers={n_ans}, explanations={n_exp}")
    if n_mcq < 25:
        errors.append(f"only {n_mcq} MCQs (<25)")

    # 2. sequential ids
    for label, ids in (("mcq-block", mcq_ids), ("explanation", exp_ids)):
        nums = sorted(int(i) for i in ids)
        if nums != list(range(1, len(nums) + 1)):
            errors.append(f"{label} ids not sequential: {nums[:30]}")

    # 3. explanation letter matches answers key
    expl_pairs = re.findall(
        r'<div class="mcq-explanation" id="exp(\d+)">.*?Correct Answer: \(([A-D])\)', html, re.S)
    seen = set()
    for n, letter in expl_pairs:
        seen.add(n)
        key = answers.get(n)
        if key is None:
            errors.append(f"exp{n}: no answers key")
        elif key.upper() != letter:
            errors.append(f"exp{n}: explanation says ({letter}) but answers key is '{key}'")
    if len(seen) != n_exp:
        errors.append(f"only {len(seen)} of {n_exp} explanations have 'Correct Answer: (X)' marker")

    # 4. score display
    m = re.search(r'id="scoreNum">0/(\d+)<', html)
    if not m:
        errors.append("scoreNum display not found")
    elif int(m.group(1)) != n_ans:
        errors.append(f"score display 0/{m.group(1)} != answers count {n_ans}")

    # 5. header count
    hm = re.search(r'MCQ Practice Set — (\d+) Questions', html)
    if not hm:
        errors.append("MCQ header count not found")
    elif int(hm.group(1)) != n_ans:
        errors.append(f"MCQ header says {hm.group(1)} but {n_ans} present")

    # 6. images exist
    imgs = re.findall(r'<img src="([^"]+)"', html)
    for src in imgs:
        if not os.path.isfile(os.path.join(BASE, src)):
            errors.append(f"image missing: {src}")
    if len(imgs) < 2:
        errors.append(f"fewer than 2 images ({len(imgs)})")

    # 7. placeholders
    for pat in [r'TODO', r'PLACEHOLDER', r'XXX', r'TBD', r'Lorem ipsum', r'FIXME']:
        if re.search(pat, html, re.I):
            errors.append(f"placeholder text found: {pat}")

    # 8. subpage links exist
    for href in re.findall(r'href="(subpages/[^"]+)"', html):
        href = href.split('#')[0]
        if not os.path.isfile(os.path.join(BASE, href)):
            errors.append(f"subpage link missing: {href}")

    # 9. radio names match block ids
    radio_names = set(re.findall(r'name="q(\d+)"', html))
    if radio_names != set(mcq_ids):
        errors.append("radio names don't match mcq-block ids")

    # 10. mandatory sections
    for sec in ["Bihar Connection", "Fact Matrix", "Cross-Topic", "Current Relevance", "Reference"]:
        if sec.lower() not in html.lower():
            errors.append(f"missing section keyword: {sec}")

    # 11. MCQ JSON sidecar
    jpath = os.path.join(BASE, "mcq", f"{slug}.json")
    if not os.path.isfile(jpath):
        errors.append(f"MCQ JSON sidecar missing: mcq/{slug}.json")
    else:
        try:
            data = json.load(open(jpath, encoding="utf-8"))
            if not isinstance(data, list) or len(data) != n_ans:
                errors.append(f"JSON sidecar has {len(data) if isinstance(data,list) else 'non-list'} items, HTML has {n_ans}")
            else:
                for i, item in enumerate(data, 1):
                    if not isinstance(item.get("q"), str) or not item["q"].strip():
                        errors.append(f"JSON q{i}: empty q")
                    opts = item.get("options")
                    if not isinstance(opts, list) or len(opts) != 4 or not all(isinstance(o, str) and o.strip() for o in opts):
                        errors.append(f"JSON q{i}: options must be 4 non-empty strings")
                    a = item.get("answer")
                    if not isinstance(a, int) or not (0 <= a <= 3):
                        errors.append(f"JSON q{i}: answer must be int 0-3, got {a!r}")
                    elif answers.get(str(i)) and "abcd"[a] != answers[str(i)]:
                        errors.append(f"JSON q{i}: answer {'abcd'[a]} != HTML key {answers[str(i)]}")
                    if not isinstance(item.get("explanation"), str) or not item["explanation"].strip():
                        errors.append(f"JSON q{i}: empty explanation")
                    if item.get("difficulty") not in ("pyq", "bpsc", "tricky"):
                        errors.append(f"JSON q{i}: bad difficulty {item.get('difficulty')!r}")
                # the check that catches a desynced answer key (see header note)
                errors.extend(check_page_sidecar_agreement(html, data))
                # answer-key balance
                _d = [0, 0, 0, 0]
                for _it in data:
                    _a = _it.get("answer")
                    if isinstance(_a, int) and 0 <= _a < 4:
                        _d[_a] += 1
                if sum(_d) and max(_d) / sum(_d) > 0.40:
                    errors.append(f"answer-key skew {_d} — {max(_d)/sum(_d)*100:.0f}% on one letter "
                                  f"(run shuffle_answers_v2.py {num})")
        except Exception as e:
            errors.append(f"JSON sidecar invalid: {e}")

    return num, slug, errors

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "all":
        nums = [int(x) for x in sys.argv[1:]]
    else:
        nums = sorted(int(os.path.basename(p).split("_")[0])
                      for p in glob.glob(os.path.join(BASE, "[0-9]*_*.html"))
                      if os.path.basename(p).split("_")[0].isdigit())
    failed = 0
    for num in nums:
        n, slug, errors = check_topic(num)
        if errors:
            failed += 1
            print(f"[{n}] {slug or '?'}: FAIL ({len(errors)} errors)")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"[{n}] {slug}: PASS")
    print(f"\n{len(nums)-failed}/{len(nums)} topics PASS")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
