#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble a timed, self-scoring mock paper from the MCQ sidecars.

    python3 build_mock.py                 # honest-size paper from what is built
    python3 build_mock.py --questions 150 # force full length (over-weights built subjects)
    python3 build_mock.py --seed 7 --name mock_02
    python3 build_mock.py --fresh         # exclude every question used in earlier mocks

Scoring mirrors BPSC: +1 correct, -1/3 wrong, 0 unattempted.

Honesty rule: the paper never silently pads a subject it cannot fill. Whatever
cannot be drawn is reported on the cover sheet and in the score breakdown, so a
mock score is never mistaken for a full-syllabus score.
"""
import json, os, re, glob, random, argparse, html as H
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
T    = os.path.join(BASE, "Topics")
OUT  = os.path.join(BASE, "mocks")

# BPSC subject distribution observed across the 69th-71st papers (sums to 149; CA absorbs the last mark)
TARGET = {"Current Affairs":31,"History":28,"Science":25,"Geography":19,
          "Bihar":16,"Polity":13,"Quant":10,"Economy":7}
GROUP2SUBJ = {
 "Current Affairs":"Current Affairs","Static GK":"Current Affairs",
 "Bihar Current Affairs":"Bihar","Bihar History":"Bihar","Bihar Geography":"Bihar",
 "Bihar Polity":"Bihar","Bihar Economy":"Bihar",
 "Modern Indian History":"History","Ancient History":"History","Medieval History":"History",
 "Biology":"Science","Chemistry":"Science","Physics":"Science",
 "Indian Geography":"Geography","World Geography":"Geography","Environment":"Geography",
 "Indian Polity":"Polity","Indian Economy":"Economy","Maths and Mental Ability":"Quant",
}
SUBJ_COLOR = {"Current Affairs":"#e94560","History":"#7c3aed","Science":"#0891b2",
              "Geography":"#059669","Bihar":"#ff6b35","Polity":"#c2185b",
              "Quant":"#64748b","Economy":"#b45309"}

def esc(x): return H.escape(str(x), quote=False)

def load_pool():
    master = {t["num"]: t for t in json.load(open(os.path.join(BASE,"topics_master.json"),encoding="utf-8"))}
    pool = {}
    for p in sorted(glob.glob(os.path.join(T,"mcq","*.json"))):
        n = int(re.match(r"\d+", os.path.basename(p)).group())
        subj = GROUP2SUBJ.get(master[n]["group"])
        if not subj: continue
        for i, q in enumerate(json.load(open(p, encoding="utf-8")), 1):
            o, a = q.get("options"), q.get("answer")
            if not isinstance(o, list) or len(o) != 4 or not isinstance(a, int): continue
            pool.setdefault(subj, []).append({
                "uid": f"{n}#{i}", "topic": n, "topic_name": master[n]["text"].split(" - ")[0],
                "subject": subj, "q": q.get("q",""), "options": o, "answer": a,
                "explanation": q.get("explanation",""), "difficulty": q.get("difficulty","bpsc")})
    return pool

def used_uids():
    seen=set()
    for p in glob.glob(os.path.join(OUT,"*.json")):
        try:
            for r in json.load(open(p,encoding="utf-8")).get("questions",[]): seen.add(r["uid"])
        except Exception: pass
    return seen

def plan_paper(pool, total, exclude):
    """total=None -> examine each subject at its FULL real weight, and simply omit
    subjects with no topics built. That keeps the surviving subjects in their true
    proportions and makes the missing block explicit, rather than quietly inflating
    whatever happens to exist."""
    avail = {s:[q for q in v if q["uid"] not in exclude] for s,v in pool.items()}
    if total is None:
        want = dict(TARGET)
    else:
        live = sum(TARGET[s] for s in TARGET if avail.get(s))
        scale = total/max(live,1)
        want = {s: (round(TARGET[s]*scale) if avail.get(s) else TARGET[s]) for s in TARGET}
    got, gaps = {}, {}
    for s,n in want.items():
        have = len(avail.get(s,[]))
        got[s] = min(n, have)
        if have < n: gaps[s] = n-have
    return want, got, gaps, avail

def build(args):
    os.makedirs(OUT, exist_ok=True)
    pool = load_pool()
    exclude = used_uids() if args.fresh else set()
    want, got, gaps, avail = plan_paper(pool, args.questions, exclude)

    rnd = random.Random(args.seed)
    picked, seen_stems = [], set()
    for s in TARGET:
        cand = avail.get(s,[])[:]
        rnd.shuffle(cand)
        take=[]
        for q in cand:
            k = re.sub(r"[^a-z0-9]","",q["q"].lower())[:70]
            if k in seen_stems: continue
            seen_stems.add(k); take.append(q)
            if len(take) >= got.get(s,0): break
        picked += take
    rnd.shuffle(picked)

    n = len(picked)
    minutes = max(20, round(n*0.8))
    name = args.name or f"mock_{len(glob.glob(os.path.join(OUT,'*.html')))+1:02d}"
    stamp = datetime.utcnow().strftime("%Y-%m-%d")

    comp = "".join(
        f"<tr><td><span class='dot' style='background:{SUBJ_COLOR[s]}'></span>{s}</td>"
        f"<td>{TARGET[s]}</td><td>{want[s]}</td><td>{got.get(s,0)}</td>"
        f"<td>{'—' if not gaps.get(s) else '<b class=gap>'+str(gaps[s])+' not built</b>'}</td></tr>"
        for s in TARGET)

    gap_note = ""
    if gaps:
        miss = ", ".join(f"{s} ({v})" for s,v in gaps.items())
        gap_note = (f"<div class='warn'><b>Coverage gap — read this before you read your score.</b> "
                    f"This paper is {n} questions, not 150, because these subjects have no topics built yet: "
                    f"{esc(miss)}. In the real paper they are worth <b>{sum(gaps.values())} marks "
                    f"({sum(gaps.values())/149*100:.0f}% of the exam)</b>. Your score below is out of {n}, "
                    f"and says nothing about how you would do on the missing {sum(gaps.values())}. "
                    f"Scale with care.</div>")

    qhtml=[]
    for i,q in enumerate(picked,1):
        opts="".join(
            f"<label class='opt'><input type='radio' name='m{i}' value='{'abcd'[k]}'> "
            f"<span class='ol'>({'ABCD'[k]})</span> {esc(o)}</label>" for k,o in enumerate(q["options"]))
        qhtml.append(
          f"<div class='q' id='m{i}' data-subj='{q['subject']}'>"
          f"<div class='qh'><span class='qn'>{i}</span>"
          f"<span class='tag' style='background:{SUBJ_COLOR[q['subject']]}'>{q['subject']}</span>"
          f"<span class='src'>topic {q['topic']}</span></div>"
          f"<div class='qt'>{esc(q['q'])}</div><div class='opts'>{opts}</div>"
          f"<div class='exp' id='e{i}'><b>Correct: ({'ABCD'[q['answer']]})</b> — {esc(q['explanation'])}"
          f"<div class='ref'>From topic {q['topic']} — {esc(q['topic_name'])}</div></div></div>")

    keys = {f"m{i}": "abcd"[q["answer"]] for i,q in enumerate(picked,1)}
    subjmap = {f"m{i}": q["subject"] for i,q in enumerate(picked,1)}

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — BPSC 72nd Prelims Mock</title><style>
*{{box-sizing:border-box}} body{{font-family:Inter,-apple-system,"Segoe UI",system-ui,sans-serif;
 background:#f1f5f9;color:#334155;margin:0;padding:24px;font-size:14px;line-height:1.6}}
.wrap{{max-width:900px;margin:0 auto}}
.head{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:26px 30px;border-radius:14px}}
.head h1{{margin:0 0 6px;font-size:23px}} .head p{{margin:0;color:#94a3b8;font-size:13px}}
.card{{background:#fff;border-radius:14px;padding:22px 26px;margin:18px 0;box-shadow:0 1px 3px rgba(0,0,0,.07)}}
table{{width:100%;border-collapse:collapse;font-size:13px}} th,td{{padding:7px 10px;border-bottom:1px solid #e2e8f0;text-align:left}}
th{{background:#f8fafc;font-weight:700;color:#1a1a2e}} .dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px}}
.gap{{color:#b91c1c}}
.warn{{background:#fff7ed;border-left:5px solid #f59e0b;padding:14px 18px;border-radius:0 10px 10px 0;margin:16px 0;font-size:13px}}
.bar{{position:sticky;top:0;z-index:20;background:#1a1a2e;color:#fff;padding:11px 18px;border-radius:11px;
 display:flex;gap:20px;align-items:center;margin:16px 0;font-size:13px;flex-wrap:wrap}}
#timer{{font-size:19px;font-weight:800;font-variant-numeric:tabular-nums}} .bar .sp{{flex:1}}
button{{border:0;border-radius:9px;padding:9px 20px;font-weight:700;cursor:pointer;font-size:13px}}
.sub{{background:#e94560;color:#fff}} .rst{{background:#475569;color:#fff}}
.q{{background:#fff;border-radius:12px;padding:17px 20px;margin:13px 0;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.qh{{display:flex;align-items:center;gap:9px;margin-bottom:8px}}
.qn{{background:#1a1a2e;color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;
 justify-content:center;font-size:12px;font-weight:700;flex:none}}
.tag{{color:#fff;padding:2px 9px;border-radius:5px;font-size:10px;font-weight:700}}
.src{{color:#94a3b8;font-size:11px;margin-left:auto}}
.qt{{font-weight:600;color:#1a1a2e;margin-bottom:10px;white-space:pre-wrap}}
.opt{{display:flex;gap:9px;padding:7px 11px;border-radius:8px;cursor:pointer}} .opt:hover{{background:#f1f5f9}}
.ol{{font-weight:700;color:#64748b;flex:none}} .opt input{{accent-color:#e94560;flex:none}}
.exp{{display:none;margin-top:10px;padding:10px 14px;background:#f0f9ff;border-left:3px solid #0ea5e9;
 border-radius:0 8px 8px 0;font-size:12.5px}} .exp.show{{display:block}}
.ref{{color:#94a3b8;font-size:11px;margin-top:6px}}
.q.ok{{border-left:4px solid #22c55e}} .q.no{{border-left:4px solid #ef4444}}
.opt.ok{{background:#dcfce7;font-weight:600}} .opt.no{{background:#fee2e2}}
#res{{display:none}} .big{{font-size:42px;font-weight:800;color:#e94560;line-height:1.1}}
@media print{{.bar,button{{display:none}} .exp{{display:block!important}} .q{{page-break-inside:avoid}} body{{background:#fff}}}}
</style></head><body><div class="wrap">
<div class="head"><h1>{name.replace('_',' ').title()} — BPSC 72nd Prelims</h1>
<p>{n} questions · {minutes} minutes · +1 correct, −⅓ wrong, 0 unattempted · generated {stamp}</p></div>

<div class="card"><b>Paper composition</b>
<table><tr><th>Subject</th><th>Real paper</th><th>Target here</th><th>Included</th><th>Shortfall</th></tr>{comp}</table>
{gap_note}
<p style="font-size:12.5px;color:#64748b;margin:12px 0 0">Reference points: the 71st cut-off for UR male was <b>88/150</b>, and good attempts were 110–130 questions. Accuracy decides this exam, not attempt count — with −⅓ negative, three wrong guesses wipe out one correct answer.</p></div>

<div class="bar"><span id="timer">{minutes:02d}:00</span><span id="prog">0 / {n} attempted</span>
<span class="sp"></span><button class="sub" onclick="submitPaper()">Submit &amp; score</button>
<button class="rst" onclick="location.reload()">Restart</button></div>

<div class="card" id="res"></div>
{''.join(qhtml)}
<div class="card" style="text-align:center"><button class="sub" onclick="submitPaper()">Submit &amp; score</button></div>
</div><script>
const KEYS={json.dumps(keys)}, SUBJ={json.dumps(subjmap)}, N={n};
let left={minutes}*60, done=false, tick=setInterval(()=>{{
  if(done) return; left--;
  if(left<=0){{clearInterval(tick); submitPaper(); return;}}
  const m=String(Math.floor(left/60)).padStart(2,'0'), s=String(left%60).padStart(2,'0');
  document.getElementById('timer').textContent=m+':'+s;
  if(left<300) document.getElementById('timer').style.color='#fca5a5';
}},1000);
document.addEventListener('change',e=>{{ if(e.target.type==='radio'){{
  const a=document.querySelectorAll('input[type=radio]:checked').length;
  document.getElementById('prog').textContent=a+' / '+N+' attempted';}}}});
function submitPaper(){{
  if(done) return; done=true; clearInterval(tick);
  let right=0,wrong=0,skip=0; const by={{}};
  for(let i=1;i<=N;i++){{
    const q=document.getElementById('m'+i), sel=q.querySelector('input:checked'), k=KEYS['m'+i], s=SUBJ['m'+i];
    by[s]=by[s]||{{r:0,w:0,s:0}};
    q.querySelectorAll('input').forEach(x=>{{if(x.value===k)x.parentElement.classList.add('ok')}});
    if(!sel){{skip++;by[s].s++;}}
    else if(sel.value===k){{right++;by[s].r++;q.classList.add('ok');}}
    else{{wrong++;by[s].w++;q.classList.add('no');sel.parentElement.classList.add('no');}}
    document.getElementById('e'+i).classList.add('show');
  }}
  const net=right-wrong/3, acc=right+wrong?(100*right/(right+wrong)):0;
  let rows='';
  Object.keys(by).sort().forEach(s=>{{const b=by[s],att=b.r+b.w;
    rows+=`<tr><td>${{s}}</td><td>${{b.r}}</td><td>${{b.w}}</td><td>${{b.s}}</td>
    <td><b>${{(b.r-b.w/3).toFixed(2)}}</b></td><td>${{att?(100*b.r/att).toFixed(0):'—'}}%</td></tr>`;}});
  document.getElementById('res').style.display='block';
  document.getElementById('res').innerHTML=
   `<div class="big">${{net.toFixed(2)}} / ${{N}}</div>
    <p style="margin:4px 0 14px;color:#64748b">${{right}} correct · ${{wrong}} wrong (−${{(wrong/3).toFixed(2)}}) · ${{skip}} unattempted · <b>${{acc.toFixed(0)}}% accuracy</b> on what you attempted</p>
    <table><tr><th>Subject</th><th>Right</th><th>Wrong</th><th>Skipped</th><th>Net</th><th>Accuracy</th></tr>${{rows}}</table>
    <p style="font-size:12.5px;color:#64748b;margin-top:14px">Scaled to a 150-mark paper this is <b>${{(net*150/N).toFixed(0)}}</b> — but only if the unbuilt subjects go as well as these did, which is an assumption, not a result. Work the wrong answers back to their source topics before the next mock.</p>`;
  document.getElementById('res').scrollIntoView({{behavior:'smooth'}});
}}
</script></body></html>"""

    hp = os.path.join(OUT, name + ".html")
    open(hp,"w",encoding="utf-8").write(doc)
    json.dump({"name":name,"generated":stamp,"count":n,"minutes":minutes,"seed":args.seed,
               "target":want,"included":got,"gaps":gaps,
               "questions":[{"n":i,"uid":q["uid"],"topic":q["topic"],"subject":q["subject"],
                             "answer":"ABCD"[q["answer"]],"difficulty":q["difficulty"]}
                            for i,q in enumerate(picked,1)]},
              open(os.path.join(OUT,name+".json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  {hp}")
    print(f"  {n} questions, {minutes} min, seed {args.seed}")
    for s in TARGET:
        g = gaps.get(s)
        print(f"    {s:16} {got.get(s,0):>3}" + (f"   <-- {g} unfillable, no topics built" if g else ""))
    if gaps: print(f"  NOTE: {sum(gaps.values())} of 149 marks ({sum(gaps.values())/149*100:.0f}%) cannot be examined yet.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", type=int, default=None)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--name")
    ap.add_argument("--fresh", action="store_true")
    build(ap.parse_args())
