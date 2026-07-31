#!/usr/bin/env python3
"""
Balance MCQ answer keys across A/B/C/D for any topic, keeping HTML and the JSON
sidecar in lockstep.

Usage:  python3 shuffle_answers_v2.py [topic_numbers...]
        python3 shuffle_answers_v2.py            # auto: every topic with >40% on one letter
        python3 shuffle_answers_v2.py --dry-run  # report only, write nothing

REWRITTEN 2026-07-31 after the previous version silently corrupted 92 questions in
topics 28, 30, 31, 32, 33. The old bugs, all now fixed:

  B1  The option-label regex only matched the `value="a"> A. Text` format. Topics
      written in the `value="a"> (A) Text` format never matched, so the HTML options
      were left untouched while the JSON was reshuffled and the HTML `const answers`
      key was rewritten to the NEW index -> the page marked a different option as
      correct than the sidecar, and than its own explanation text.
  B2  Skew detection only looked at answer 'a' (`dist['a'] > 15`). A topic that was
      80% 'b' was reported as "already balanced" and skipped.
  B3  The answers-object regex hardcoded `q1:.*?q25:`, so topics with 33-34 MCQs
      were not updated at all.
  B4  Per-question random.shuffle() gives a random, not balanced, distribution.
  B5  A single module-level random.seed(42) made every topic produce the same
      permutation sequence (topics 69/70/71/142 all landed on 5A/2B/8C/10D).
  B6  Failures were silent: the JSON was written even when the HTML rewrite failed.
  B7  Marker stripping was position-blind, so an option like "C. Rangarajan" sitting
      at position (D) was read as marker "C." + text "Rangarajan".

Guarantees now: every write is all-or-nothing; HTML option text, HTML answer key,
HTML explanation letter and the JSON sidecar are always updated together, or the
topic is skipped and reported.
"""

import json, os, re, glob, random, sys, html as H, unicodedata

TOPICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Topics")
MCQ_DIR = os.path.join(TOPICS_DIR, "mcq")
SKEW_LIMIT = 0.40

LABEL_RE = re.compile(
    r'(<label class="mcq-option"><input type="radio" name="q(\d+)" value=")'
    r'([abcd])("\s*>)(.*?)(</label>)', re.S)
# NOTE: requires whitespace after the marker, otherwise initials such as
# "C.P. Radhakrishnan", "A.O. Hume", "R.C. Dutt" get mangled into "P. Radhakrishnan".
PREFIX_RE = re.compile(r'^\s*(?:\(([A-D])\)|([A-D])[.)])\s+')


def plain(s):
    s = re.sub(r'<br\s*/?>', ' ', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', H.unescape(s).replace('\xa0', ' ')).strip()


def strip_marker(s, idx=None):
    """Drop a leading option marker, but only when it matches the option's own
    position — otherwise initials like "C. Rangarajan" sitting at position D get
    mangled into "Rangarajan" and HTML/JSON comparison falsely fails (B7)."""
    m = PREFIX_RE.match(s)
    if not m:
        return s.strip()
    letter = m.group(1) or m.group(2)
    if idx is not None and letter != "ABCD"[idx]:
        return s.strip()
    return s[m.end():].strip()


def norm(s, idx=None):
    s = unicodedata.normalize('NFKD', str(s))
    return re.sub(r'[^a-z0-9]', '', strip_marker(s, idx).lower())


def find_files(num):
    h = glob.glob(os.path.join(TOPICS_DIR, f"{num}_*.html"))
    j = glob.glob(os.path.join(MCQ_DIR, f"{num}_*.json"))
    return (h[0], j[0]) if h and j else (None, None)


def load_questions(json_path):
    d = json.load(open(json_path, encoding="utf-8"))
    return d.get("questions", []) if isinstance(d, dict) else d


def distribution(qs):
    d = [0, 0, 0, 0]
    for q in qs:
        a = q.get("answer")
        if isinstance(a, int) and 0 <= a < 4:
            d[a] += 1
    return d


def balanced_targets(n, seed):
    """Round-robin A/B/C/D, shuffled — guarantees near-perfect balance (B4)."""
    rnd = random.Random(seed)
    t = [i % 4 for i in range(n)]
    rnd.shuffle(t)
    return t


def detect_style(inner):
    if not PREFIX_RE.match(inner):
        return "(%s) "
    return "(%s) " if inner.lstrip().startswith("(") else "%s. "


def shuffle_topic(num, dry_run=False):
    html_path, json_path = find_files(num)
    if not html_path:
        print(f"  x Topic {num}: files not found"); return False

    qs = load_questions(json_path)
    dist = distribution(qs)
    total = sum(dist)
    if not total:
        print(f"  x Topic {num}: no usable answers"); return False
    if max(dist) / total <= SKEW_LIMIT:                                   # B2
        print(f"  = Topic {num}: balanced {dist} ({max(dist)/total*100:.0f}%) — skip"); return True

    html = open(html_path, encoding="utf-8").read()
    targets = balanced_targets(len(qs), seed=num)                          # B4/B5
    plan, new_answers = [], {}

    for i, q in enumerate(qs, 1):
        opts = q.get("options") or []
        ans = q.get("answer")
        if len(opts) != 4 or not isinstance(ans, int):
            print(f"  x Topic {num}: q{i} malformed — ABORT, nothing written"); return False
        blk = re.search(
            r'(<div class="mcq-block" id="q%d">)(.*?)(?=<div class="mcq-block" id="q\d+">'
            r'|<div class="answer-key|</body>)' % i, html, re.S)
        if not blk:
            print(f"  x Topic {num}: q{i} block not found — ABORT"); return False
        labels = list(LABEL_RE.finditer(blk.group(2)))
        if len(labels) != 4:                                               # B1/B6
            print(f"  x Topic {num}: q{i} has {len(labels)} option labels — ABORT"); return False
        pool = {}
        for m in labels:
            k = "abcd".index(m.group(3))
            inner = m.group(5)
            pool[norm(plain(inner), k)] = strip_marker(inner, k)
        if set(pool) != {norm(o, k) for k, o in enumerate(opts)}:          # B6
            print(f"  x Topic {num}: q{i} HTML/JSON option sets differ — ABORT"); return False

        correct = opts[ans]
        others = [o for j, o in enumerate(opts) if j != ans]
        rnd = random.Random(num * 1000 + i)
        rnd.shuffle(others)
        tgt = targets[i - 1]
        new_opts = others[:tgt] + [correct] + others[tgt:]
        plan.append((i, blk, labels, pool, new_opts, tgt, detect_style(labels[0].group(5))))
        new_answers[i] = "abcd"[tgt]
        q["options"], q["answer"] = new_opts, tgt

    if dry_run:
        print(f"  ~ Topic {num}: would rebalance {dist} -> {distribution(qs)}"); return True

    # --- apply to HTML (all-or-nothing; blocks rewritten back-to-front) ---
    for i, blk, labels, pool, new_opts, tgt, style in reversed(plan):
        body = blk.group(2)
        for k in range(3, -1, -1):
            m = labels[k]
            letter, val = "ABCD"[k], "abcd"[k]
            inner = " " + (style % letter) + pool[norm(new_opts[k], k)]
            body = body[:m.start()] + m.group(1) + val + m.group(4) + inner + m.group(6) + body[m.end():]
        body = re.sub(r'(id="exp%d">.{0,60}?Correct Answer:\s*\()[A-D](\))' % i,
                      lambda mm: mm.group(1) + "ABCD"[tgt] + mm.group(2), body, count=1, flags=re.S)
        html = html[:blk.start(2)] + body + html[blk.end(2):]

    km = re.search(r'(const answers\s*=\s*\{)(.*?)(\};)', html, re.S)       # B3
    if not km:
        print(f"  x Topic {num}: answers object not found — ABORT"); return False
    body = km.group(2)
    for i, letter in new_answers.items():
        body, n = re.subn(r"(\bq%d\s*:\s*')[abcd](')" % i,
                          lambda mm: mm.group(1) + letter + mm.group(2), body, count=1)
        if not n:
            print(f"  x Topic {num}: q{i} missing from answers object — ABORT"); return False
    html = html[:km.start(2)] + body + html[km.end(2):]

    open(html_path, "w", encoding="utf-8").write(html)
    json.dump(qs, open(json_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  + Topic {num}: {dist} -> {distribution(qs)}")
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if args:
        topics = [int(x) for x in args]
    else:
        topics = []
        for n in range(1, 160):
            _, j = find_files(n)
            if not j: continue
            d = distribution(load_questions(j))
            if sum(d) and max(d) / sum(d) > SKEW_LIMIT:
                topics.append(n)
        if not topics:
            print("No topics exceed the skew limit."); return
    print(f"{'Dry run over' if dry else 'Rebalancing'} {len(topics)} topics: {topics}\n" + "=" * 60)
    ok = sum(bool(shuffle_topic(n, dry)) for n in topics)
    print(f"\n{ok}/{len(topics)} succeeded.")


if __name__ == "__main__":
    main()
