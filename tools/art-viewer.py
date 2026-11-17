#!/usr/bin/env python3
"""Live art viewer: watch the art pipeline from a browser while the makers work.

    python3 tools/art-viewer.py            -> http://localhost:8765
    python3 tools/art-viewer.py --port 9000

Nothing has to report to it. It watches the files the pipeline already writes:
  - art/candidates/**            every candidate, comparison sheet and copied in-game shot
  - .art-runs/*/build/...        in-game screenshots and logs of runs that are going now (ART_RUN=<name>)
  - mod/build/smoke-run/...      the main in-game run
  - mod/.../textures/item|block  what is installed in the mod
  - git                          what is committed (accepted) and what is installed but not yet committed
  - docs/Decisions/              the owner's decisions, newest first
A candidate that is byte-identical to the installed texture is marked as the pick; the others are "not picked".
Serves on localhost only. Python standard library only.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "mod/src/main/resources/assets/mimcontent/textures"
WATCH = [ROOT / "art/candidates", ROOT / ".art-runs", ROOT / "mod/build/smoke-run/screenshots", TEX]
DECISIONS = ROOT / "docs/Decisions"
IMG = (".png", ".jpg", ".jpeg", ".webp", ".gif")

state = {"version": 0, "data": {}}
cond = threading.Condition()
_hash_cache = {}


def md5(p, mtime):
    key = (str(p), mtime)
    if key not in _hash_cache:
        try:
            _hash_cache[key] = hashlib.md5(p.read_bytes()).hexdigest()
        except OSError:
            _hash_cache[key] = None
    return _hash_cache[key]


def rel(p):
    return str(p.relative_to(ROOT))


def scan_files():
    out = []
    for base in WATCH:
        if not base.exists():
            continue
        for dirpath, dirnames, files in os.walk(base):
            # in .art-runs only the screenshots and logs matter (skip the copied sources, Gradle caches, saves)
            if ".art-runs" in dirpath:
                dirnames[:] = [d for d in dirnames if d in ("build", "smoke-run", "screenshots")
                               or Path(dirpath).parent.name == ".art-runs"]
            for f in files:
                if f.lower().endswith(IMG) or (f == "smoke.log" and ".art-runs" in dirpath):
                    p = Path(dirpath) / f
                    try:
                        st = p.stat()
                    except OSError:
                        continue
                    out.append((p, st.st_mtime, st.st_size))
    return out


def git_info():
    try:
        tracked = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.split("\n"))
        dirty = set()
        for line in subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.splitlines():
            path = line[3:].strip().strip('"')
            dirty.add(path)
        log = subprocess.run(["git", "log", "-12", "--format=%h|%cr|%s"], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout
        commits = [dict(zip(("hash", "when", "subject"), l.split("|", 2))) for l in log.splitlines() if l.count("|") >= 2]
        return tracked, dirty, commits
    except Exception:
        return set(), set(), []


def running_runs():
    try:
        out = subprocess.run(["pgrep", "-af", "run-art.sh"], capture_output=True, text=True, timeout=5).stdout
    except Exception:
        return []
    runs = []
    for d in sorted((ROOT / ".art-runs").glob("*")) if (ROOT / ".art-runs").exists() else []:
        log = d / "build/smoke.log"
        live = False
        for pid in out.splitlines():
            pass
        tail = ""
        if log.exists():
            try:
                lines = log.read_text(errors="replace").splitlines()
                keep = [l for l in lines if re.search(r"\[smoke\]|BUILD|FAILED|Exception|error:", l)]
                tail = "\n".join(keep[-4:])[-600:]
                live = time.time() - log.stat().st_mtime < 20 and "BUILD" not in (keep[-1] if keep else "")
            except OSError:
                pass
        runs.append({"name": d.name, "live": live, "tail": tail,
                     "mtime": log.stat().st_mtime if log.exists() else d.stat().st_mtime})
    any_main = "run-art.sh" in out
    return sorted(runs, key=lambda r: -r["mtime"]), any_main


def decisions():
    out = []
    if not DECISIONS.exists():
        return out
    for p in sorted(DECISIONS.glob("*.md"), key=lambda p: -p.stat().st_mtime)[:25]:
        text = p.read_text(errors="replace")
        m = re.search(r'^quote:\s*"?(.*?)"?\s*$', text, re.M)
        out.append({"title": p.stem, "quote": (m.group(1) if m else "").replace('\\"', '"'), "mtime": p.stat().st_mtime})
    return out


SUFFIX = re.compile(r"(_compare|_plain|_x2|_fresh|_cake|_icon\d*|_owner.*|_[a-z]|_v\d+[a-z]?|_\d+)$")


def group_of(p, items):
    """Which food a file belongs to: the longest installed item/block name its name or folder starts with."""
    parts = p.relative_to(ROOT).parts
    name = p.stem.lower()
    folder = p.parent.name.lower()
    if folder.startswith("ingame_"):
        name = folder[7:]
    elif ".art-runs" in parts:
        return "in-game: " + parts[parts.index(".art-runs") + 1]
    elif p.parent.name == "screenshots":
        return "in-game: main run"
    best = ""
    for it in items:
        if (name == it or name.startswith(it + "_") or name.startswith(it)) and len(it) > len(best):
            best = it
    if best:
        return best
    while SUFFIX.search(name):
        name = SUFFIX.sub("", name)
    return name or p.stem


def build():
    files = scan_files()
    tracked, dirty, commits = git_info()
    installed = {}
    for p, mt, sz in files:
        if TEX in p.parents and p.suffix == ".png":
            kind = p.parent.name
            if kind not in ("item", "block"):
                continue
            r = rel(p)
            installed[r] = {"path": r, "kind": kind, "name": p.stem, "mtime": mt, "hash": md5(p, mt),
                            "committed": r in tracked and r not in dirty, "pending": r in dirty or r not in tracked}
    item_names = sorted({v["name"] for v in installed.values() if v["kind"] == "item"}
                        | {re.sub(r"_(top|side|inside|bottom|plate|handle|eaten\d)$", "", v["name"]) for v in installed.values()},
                        key=len, reverse=True)
    inst_hash = {}
    for v in installed.values():
        inst_hash.setdefault(v["hash"], []).append(v["path"])

    groups = {}
    feed = []
    for p, mt, sz in files:
        r = rel(p)
        if r in installed:
            continue
        g = group_of(p, item_names)
        if p.name == "smoke.log":
            continue
        kind = ("in-game" if ("ingame_" in r or "screenshots" in r) else
                "sheet" if "compare" in p.stem or "sheet" in p.stem else "candidate")
        e = {"path": r, "mtime": mt, "kind": kind, "group": g}
        if kind == "candidate" and p.suffix == ".png":
            h = md5(p, mt)
            e["pick"] = h in inst_hash
        groups.setdefault(g, {"name": g, "files": [], "last": 0})
        groups[g]["files"].append(e)
        groups[g]["last"] = max(groups[g]["last"], mt)
        feed.append(e)

    for v in installed.values():
        base = re.sub(r"_(top|side|inside|bottom|plate|handle|eaten\d)$", "", v["name"])
        g = groups.setdefault(base, {"name": base, "files": [], "last": 0})
        g.setdefault("installed", []).append(v)
        g["last"] = max(g["last"], v["mtime"])

    for g in groups.values():
        g["files"].sort(key=lambda e: -e["mtime"])
        inst = g.get("installed", [])
        if not inst:
            g["status"] = "in game run" if g["name"].startswith("in-game") else "candidates only"
        elif all(i["committed"] for i in inst):
            g["status"] = "accepted (committed)"
        else:
            g["status"] = "in the mod, waiting for the owner"
    feed.sort(key=lambda e: -e["mtime"])
    runs, any_run = running_runs()
    return {"groups": sorted(groups.values(), key=lambda g: -g["last"]), "feed": feed[:80],
            "runs": runs, "anyRun": any_run, "commits": commits, "decisions": decisions(), "now": time.time()}


def watcher():
    last_sig = None
    tick = 0
    while True:
        try:
            files = scan_files()
            sig = hash(tuple((str(p), m, s) for p, m, s in files)) ^ hash(tuple(
                p.stat().st_mtime for p in DECISIONS.glob("*.md"))) if DECISIONS.exists() else 0
            tick += 1
            if sig != last_sig or tick % 10 == 0:   # also refresh git/run state every ~15 s
                data = build()
                with cond:
                    if json.dumps(data, sort_keys=True, default=str) != json.dumps(state["data"], sort_keys=True, default=str):
                        state["data"] = data
                        state["version"] += 1
                        cond.notify_all()
                last_sig = sig
        except Exception as ex:  # keep watching whatever happens
            print("watch error:", ex)
        time.sleep(1.5)


PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MiM art live</title><style>
:root{--bg:#f4f1ea;--card:#fff;--ink:#1d1b18;--mute:#6b665d;--line:#e2ddd2;--acc:#b5532a;--ok:#2f7d4a;--wait:#b7791f;--no:#8a8478;--slot:#8b8b8b}
@media (prefers-color-scheme:dark){:root{--bg:#16140f;--card:#211e18;--ink:#eee8dc;--mute:#a59e90;--line:#353027;--acc:#e07a4a;--ok:#5cb87a;--wait:#e0a84a;--no:#7d776b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
h1{font-size:17px;margin:0}.dot{width:9px;height:9px;border-radius:50%;background:var(--no);display:inline-block}.live .dot{background:var(--ok);box-shadow:0 0 0 3px #2f7d4a33}
nav button{background:none;border:1px solid var(--line);color:var(--ink);padding:4px 10px;border-radius:14px;cursor:pointer}nav button.on{background:var(--ink);color:var(--bg)}
main{padding:14px 16px;max-width:1500px;margin:0 auto}.cols{display:grid;grid-template-columns:1fr 330px;gap:16px}@media(max-width:900px){.cols{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-bottom:14px}
.card h2{font-size:15px;margin:0 0 2px}.st{font-size:12px;color:var(--mute)}.badge{font-size:11px;padding:1px 7px;border-radius:9px;border:1px solid currentColor;margin-left:6px}
.b-ok{color:var(--ok)}.b-wait{color:var(--wait)}.b-no{color:var(--no)}.b-new{color:var(--acc)}
.row{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}.tile{text-align:center;font-size:11px;color:var(--mute);max-width:150px;cursor:zoom-in}
.px{image-rendering:pixelated;background:var(--slot);border-radius:4px;display:block;margin:0 auto 3px}.ico{width:96px;height:96px}
.pick .px{outline:3px solid var(--ok)}.rej .px{opacity:.55}.rej .px:hover{opacity:1}
.sheet{max-width:100%;max-height:340px;border-radius:6px;border:1px solid var(--line);cursor:zoom-in;display:block;margin-top:8px;background:#fff}
.shots{display:flex;gap:8px;overflow-x:auto;margin-top:8px}.shots img{height:120px;border-radius:5px;cursor:zoom-in}
.feed .tile{max-width:84px}.feed .ico{width:64px;height:64px}.age{font-size:10px}
.side h3{font-size:13px;margin:0 0 6px}.dec{border-left:3px solid var(--acc);padding:3px 8px;margin:7px 0;font-size:12px}.dec b{display:block;font-size:12px}
pre{white-space:pre-wrap;font-size:11px;color:var(--mute);margin:4px 0 0}
#zoom{position:fixed;inset:0;background:#000d;display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}#zoom img{max-width:95vw;max-height:92vh;image-rendering:pixelated;background:var(--slot)}
.empty{color:var(--mute);padding:20px}
</style></head><body>
<header><h1>MiM art, live</h1><span id="conn"><span class="dot"></span> <span id="connt">connecting</span></span>
<nav><button data-v="foods" class="on">By food</button><button data-v="feed">Newest first</button></nav>
<span class="st" id="sum"></span></header>
<main><div class="cols"><div id="view"></div><aside class="side" id="side"></aside></div></main>
<div id="zoom"><img></div>
<script>
let D=null,view="foods",seen=new Set(),first=true;
const f=p=>"/file?p="+encodeURIComponent(p)+"&t="+Math.round(Date.now()/60000);
const ago=t=>{let s=(D?D.now:Date.now()/1000)-t;return s<60?Math.round(s)+"s ago":s<3600?Math.round(s/60)+" min ago":s<86400?Math.round(s/3600)+" h ago":Math.round(s/86400)+" d ago"};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const base=p=>p.split("/").pop();
function tile(e,cls){const isNew=!first&&!seen.has(e.path+e.mtime);return `<div class="tile ${cls||""}" data-z="${esc(e.path)}"><img class="px ico" loading="lazy" src="${f(e.path)}">${esc(base(e.path))}${isNew?'<span class="badge b-new">new</span>':""}<div class="age">${ago(e.mtime)}</div></div>`}
function group(g){
 const inst=(g.installed||[]).filter(i=>i.kind==="item"),blk=(g.installed||[]).filter(i=>i.kind==="block");
 const cands=g.files.filter(e=>e.kind==="candidate"),sheets=g.files.filter(e=>e.kind==="sheet"),shots=g.files.filter(e=>e.kind==="in-game");
 const sc=g.status.startsWith("accepted")?"b-ok":g.status.startsWith("in the mod")?"b-wait":"b-no";
 let h=`<div class="card"><h2>${esc(g.name)}<span class="badge ${sc}">${esc(g.status)}</span></h2><div class="st">last change ${ago(g.last)}</div>`;
 if(inst.length||blk.length) h+=`<div class="row">${inst.map(i=>tile(i,"pick")).join("")}${blk.slice(0,6).map(i=>tile(i)).join("")}</div>`;
 if(cands.length) h+=`<div class="st" style="margin-top:8px">candidates (green = the installed pick, faded = not picked)</div><div class="row">${cands.slice(0,24).map(e=>tile(e,e.pick?"pick":"rej")).join("")}</div>`;
 if(sheets.length) h+=`<img class="sheet" data-z="${esc(sheets[0].path)}" src="${f(sheets[0].path)}"><div class="st">${esc(base(sheets[0].path))}, ${ago(sheets[0].mtime)}${sheets.length>1?` (+${sheets.length-1} older sheets)`:""}</div>`;
 if(shots.length) h+=`<div class="shots">${shots.slice(0,10).map(e=>`<img data-z="${esc(e.path)}" src="${f(e.path)}" title="${esc(base(e.path))}">`).join("")}</div>`;
 return h+"</div>"}
function render(){
 if(!D)return;const v=document.getElementById("view");
 if(view==="foods"){const gs=D.groups.filter(g=>!g.name.startsWith("in-game"));v.innerHTML=gs.length?gs.map(group).join(""):'<div class="empty">Nothing yet.</div>';
  const runs=D.groups.filter(g=>g.name.startsWith("in-game"));if(runs.length)v.innerHTML+=runs.map(group).join("")}
 else v.innerHTML=`<div class="card feed"><h2>Newest files</h2><div class="row">${D.feed.map(e=>tile(e,e.kind==="candidate"?(e.pick?"pick":""):"")).join("")}</div></div>`;
 const live=D.runs.filter(r=>r.live);
 document.getElementById("side").innerHTML=
  `<div class="card"><h3>In-game test runs</h3>${D.runs.length?D.runs.slice(0,6).map(r=>`<div><b>${esc(r.name)}</b> <span class="badge ${r.live?"b-wait":"b-no"}">${r.live?"running":"done"}</span> <span class="st">${ago(r.mtime)}</span><pre>${esc(r.tail)}</pre></div>`).join(""):'<span class="st">none yet</span>'}</div>`+
  `<div class="card"><h3>Owner decisions</h3>${D.decisions.map(d=>`<div class="dec"><b>${esc(d.title.replace(/^\d{4}-\d\d-\d\d /,""))}</b>${esc(d.quote).slice(0,220)}<div class="age">${ago(d.mtime)}</div></div>`).join("")}</div>`+
  `<div class="card"><h3>Commits</h3>${D.commits.map(c=>`<div class="st"><b style="color:var(--ink)">${esc(c.subject)}</b> ${esc(c.when)}</div>`).join("")}</div>`;
 document.getElementById("sum").textContent=`${D.groups.filter(g=>g.status.startsWith("accepted")).length} accepted · ${D.groups.filter(g=>g.status.startsWith("in the mod")).length} waiting for you · ${live.length} test run${live.length==1?"":"s"} going`;
 D.feed.forEach(e=>seen.add(e.path+e.mtime));D.groups.forEach(g=>(g.installed||[]).forEach(e=>seen.add(e.path+e.mtime)));first=false}
async function load(){D=await (await fetch("/state.json")).json();render()}
function connect(){const es=new EventSource("/events");const c=document.getElementById("conn"),t=document.getElementById("connt");
 es.onopen=()=>{c.className="live";t.textContent="live"};es.onmessage=()=>load();es.onerror=()=>{c.className="";t.textContent="reconnecting"}}
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{view=b.dataset.v;document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x===b));try{localStorage.setItem("view",view)}catch(e){}render()});
try{const s=localStorage.getItem("view");if(s)document.querySelector(`nav button[data-v="${s}"]`)?.click()}catch(e){}
document.addEventListener("click",e=>{const z=e.target.closest("[data-z]");const Z=document.getElementById("zoom");
 if(z){Z.querySelector("img").src=f(z.dataset.z);Z.style.display="flex"}else if(e.target.closest("#zoom"))Z.style.display="none"});
load();connect();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            return self.send(200, PAGE.encode(), "text/html; charset=utf-8")
        if u.path == "/state.json":
            with cond:
                data = state["data"]
            return self.send(200, json.dumps(data, default=str).encode(), "application/json")
        if u.path == "/file":
            p = (ROOT / parse_qs(u.query).get("p", [""])[0]).resolve()
            ok = any(p == w or w.resolve() in p.parents for w in WATCH) and p.suffix.lower() in IMG and p.is_file()
            if not ok:
                return self.send(404, b"not found", "text/plain")
            ctype = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}[p.suffix.lower()]
            return self.send(200, p.read_bytes(), ctype)
        if u.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            seen = -1
            try:
                while True:
                    with cond:
                        cond.wait_for(lambda: state["version"] != seen, timeout=20)
                        v = state["version"]
                    if v != seen:
                        self.wfile.write(f"data: {v}\n\n".encode())
                        seen = v
                    else:
                        self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                return
        return self.send(404, b"not found", "text/plain")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    state["data"] = build()
    threading.Thread(target=watcher, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"art viewer: http://localhost:{a.port}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
