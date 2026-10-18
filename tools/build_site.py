"""Generate the site pages that aren't forms: the landing page, the forms index, How to read,
and the technique library (/library/ and one page per family).

usage: python3 tools/build_site.py

Reads data/catalog.json (which forms exist), data/techniques.json (the library) and every
forms/*.json (for "appears in" lists and the figures). Run it after building or changing a form;
build_form.py --all runs it too.
"""
import json, os, re
import sitekit as S
from sitekit import ROOT, esc

LIB, CAT = S.LIB, S.CATALOG
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700;900&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">')
ICON = ("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 rx=%223%22 "
        "fill=%22%231f3a8a%22/%3E%3Cpath d=%22M3 4h10M3 8h10M3 12h10%22 stroke=%22white%22 stroke-width=%221.6%22/%3E%3C/svg%3E")

# ---------------------------------------------------------------- data
FORMS = [json.load(open(p, encoding="utf-8")) for p in S.form_files()]
LIVE = {F["slug"] for F in FORMS}
BY_SLUG = {F["slug"]: F for F in FORMS}
HEIGHT = {"low": "Low · arae", "middle": "Middle · momtong", "high": "High · eolgul"}

def appears(field, key):
    """[(form, [move ids])] in teaching order, for moves whose `field` is `key`."""
    out = []
    for F in FORMS:
        ids = [m["id"] for m in F["moves"] if m[field] == key]
        if ids: out.append((F, ids))
    return out

def demo(field, key):
    """The move a library entry is drawn from: its first appearance, preferring a side view
    (techniques read best in profile)."""
    hits = [m for F in FORMS for m in F["moves"] if m[field] == key]
    if not hits: return None
    return next((m for m in hits if m["view"] == "side"), hits[0])

def stance_demo(key, view):
    """A clean stance figure: fists chambered, so only the legs carry information."""
    m = {"id": "x", "stance": key, "lead": "L", "arms": {}, "tech": "junbi"}
    if view == "side": m.update(view="side", face="R", dir="da1")
    else: m.update(view="front", dir="ga")
    if key == "ready": m["arms"] = {"L": "junbi", "R": "junbi"}
    if key == "crane": m["lead"] = "R"
    return m

def surface_users(key):
    return [k for k, t in LIB["techniques"].items() if t.get("surface") == key and appears("tech", k)]

# ---------------------------------------------------------------- page shell
def page(path, title, desc, body, css="", js="", active=None, figures=False):
    scripts = ""
    if figures or js:
        lib = f"const LIB={S.lib_js()};\n" + (S.read("templates/figure.js") if figures else "")
        scripts = f"<script>\n(function(){{\n{lib}\n{js}\n}})();\n</script>"
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{ICON}">
{FONTS}
<style>
body{{margin:0}}[hidden]{{display:none!important}}img{{max-width:100%}}
{S.read("templates/base.css")}
.wrap{{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:28px 56px;display:flex;flex-direction:column;gap:30px}}
.eyebrow{{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.1em;color:var(--fire);text-transform:uppercase}}
h1{{margin:4px 0 0;font-family:var(--f-display);font-weight:900;font-size:clamp(36px,6vw,60px);line-height:1.05;letter-spacing:-.01em}}
h1 span{{font-weight:700;color:var(--muted);font-size:.55em;margin-left:.3em}}
h2{{margin:0 0 10px;font-family:var(--f-display);font-weight:700;font-size:26px;line-height:1.2}}
h2 span{{font-weight:700;color:var(--muted);font-size:.7em;margin-left:.3em}}
.lede{{margin:12px 0 0;max-width:64ch;color:var(--muted);font-size:16.5px}}
section > p.intro{{margin:0 0 16px;color:var(--muted);max-width:68ch}}
.pill{{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:99px;white-space:nowrap}}
.pill.live{{background:var(--ink);color:var(--surface)}}
.pill.plan{{border:1.5px solid var(--line);color:var(--muted)}}
{css}
</style>
</head>
<body>
<div class="wrap">
{S.nav(active)}
{body}
{S.footer()}
</div>
{scripts}
</body>
</html>
"""
    out = os.path.join(ROOT, "site", path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("page ->", os.path.relpath(out, ROOT))

def tri(lines, cls="tri"):
    return f'<div class="{cls}" aria-hidden="true">' + "".join(
        f'<div class="bar">{"<i></i>" if l else "<i></i><i></i>"}</div>' for l in lines) + "</div>"

def form_title(c):
    return f'Taegeuk {c["rom"]}' if "n" in c else c["rom"]

# ---------------------------------------------------------------- forms index (/forms/)
FORMS_CSS = """
header.top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px 32px;align-items:end}
.status{display:flex;flex-direction:column;gap:16px;min-width:220px}
.status b{font-family:var(--f-mono);font-weight:500;font-size:26px;font-variant-numeric:tabular-nums}
.status small{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.meter{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:4px}
.meter i{height:6px;border-radius:3px;background:var(--line)}
.meter i.done{background:var(--fire)}
.grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 18px 16px;display:flex;flex-direction:column;gap:12px;min-height:236px;color:inherit;text-decoration:none;transition:border-color .2s,transform .2s}
a.card:hover{border-color:var(--heaven);transform:translateY(-2px)}
a.card:focus-visible{outline:2px solid var(--heaven);outline-offset:3px}
.card.soon{background:transparent;border-style:dashed}
.card .top{display:flex;justify-content:space-between;align-items:flex-start}
.num{font-family:var(--f-display);font-weight:900;font-size:44px;line-height:.9}
.card.soon .num{color:var(--muted)}
.tri{display:flex;flex-direction:column;gap:6px;width:58px;padding-top:4px}
.tri .bar{display:flex;gap:8px;height:8px}
.tri .bar i{flex:1;background:var(--heaven);border-radius:2px}
.card.soon .tri .bar i{background:var(--muted);opacity:.55}
.name{display:flex;flex-direction:column;gap:2px}
.name h3{margin:0;font-size:20px;font-weight:700;letter-spacing:.01em}
.name .ko{font-family:var(--f-display);font-weight:700;color:var(--muted);font-size:15px}
.mean{margin:0;font-size:14px;color:var(--muted)}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:13px}
.foot .mv{font-family:var(--f-mono);color:var(--muted);font-variant-numeric:tabular-nums}
.bb{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:8px}
.bb li{border:1px dashed var(--line);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column}
.bb b{font-weight:600}
.bb span{font-size:12.5px;color:var(--muted)}
.bb a{display:flex;flex-direction:column;gap:2px;color:inherit;text-decoration:none;border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:10px 12px;margin:-11px -13px;transition:border-color .2s}
.bb a:hover{border-color:var(--ink)}
.bb a:focus-visible{outline:2px solid var(--heaven);outline-offset:2px}
.bb li.live{border-style:solid;border-color:transparent}
.bb .hj{font-family:var(--f-display);font-weight:900;color:var(--heaven);font-size:15px}
.bb .row{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:4px}
.bb .ko{font-family:var(--f-display);font-weight:700}
.status > div{display:flex;flex-direction:column;gap:6px}
.jump{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 0}
.jump a{font-weight:600;font-size:14px;text-decoration:none;color:var(--ink);padding:6px 14px;border-radius:99px;border:1px solid var(--line);background:var(--surface)}
.jump a:hover{border-color:var(--ink)}
.family{display:flex;flex-direction:column;gap:0;scroll-margin-top:16px}
.family > h2{font-size:30px;padding-top:14px;border-top:2px solid var(--ink)}
.family > .intro{margin:0 0 6px}
h3.sub{margin:22px 0 12px;font-family:var(--f-display);font-weight:700;font-size:21px}
h3.sub span{font-weight:700;color:var(--muted);font-size:.72em;margin-left:.3em}
.dia{width:58px;height:58px;flex:none}
.dia path{fill:none;stroke:var(--heaven);stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}
.dia circle{fill:var(--fire)}
.card.soon .dia path{stroke:var(--muted);opacity:.7}
.card a.off{font-size:13px;align-self:flex-start;margin-top:-4px}
.family .refs{margin-top:8px}
.family .note{margin:12px 0 0;font-size:14px;max-width:80ch}
@media (max-width:640px){header.top{grid-template-columns:1fr}.card{min-height:0}}
"""

WT = CAT["taegeuk"] + CAT["blackbelt"]     # World Taekwondo (Kukkiwon) poomsae
ITF = CAT["itf"]                            # ITF (Chang Hon) tul

def meter(allf=WT):
    live = sum(c["slug"] in LIVE for c in allf)
    bars = "".join(f'<i class="{"done" if c["slug"] in LIVE else ""}"></i>' for c in allf)
    return live, len(allf), f'<div class="meter" style="--n:{len(allf)}">{bars}</div>'

def taegeuk_cards():
    out = []
    for c in CAT["taegeuk"]:
        live = c["slug"] in LIVE
        pill = '<span class="pill live">Open</span>' if live else '<span class="pill plan">Planned</span>'
        inner = (f'<div class="top"><span class="num">{c["n"]}</span>{tri(c["lines"])}</div>'
                 f'<div class="name"><h3>{c["rom"]}</h3><span class="ko">{c["ko"]} · {c["tri"]} {c["triKo"]} · {c["sym"]}</span></div>'
                 f'<p class="mean">{c["mean"]}</p><div class="foot"><span class="mv">{c["moves"]} movements</span>{pill}</div>')
        out.append(f'<li><a class="card" href="/{c["slug"]}/" aria-label="Open Taegeuk {c["rom"]}">{inner}</a></li>' if live
                   else f'<li><div class="card soon">{inner}</div></li>')
    return "".join(out)

def bb_cards():
    out = []
    for c in CAT["blackbelt"]:
        if c["slug"] in LIVE:
            out.append(f'<li class="live"><a href="/{c["slug"]}/" aria-label="Open {c["rom"]}"><b>{c["rom"]} <span class="hj" lang="zh-Hant">{c["hanja"]}</span></b>'
                       f'<span><span class="ko">{c["ko"]}</span> · floor line {c["floor"]}</span><span class="row"><span>{c["moves"]} movements</span><span class="pill live">Open</span></span></a></li>')
        else:
            out.append(f'<li><b>{c["rom"]}</b><span><span class="ko">{c["ko"]}</span> · planned</span></li>')
    return "".join(out)

def diagram(c, cls="dia"):
    """An ITF pattern's floor line (its skeleton layout) from catalog `diagram`: `d` is an SVG path on a
    40x40 grid with A at the top, `start` the ready position."""
    D = c.get("diagram")
    if not D: return f'<div class="{cls}" aria-hidden="true"></div>'
    x, y = D["start"]
    return (f'<svg class="{cls}" viewBox="-4 -4 48 48" aria-hidden="true"><path d="{D["d"]}"/>'
            f'<circle cx="{x}" cy="{y}" r="3.4"/></svg>')

def itf_cards(group):
    out = []
    for c in ITF:
        if c["group"] != group: continue
        live = c["slug"] in LIVE
        pill = '<span class="pill live">Open</span>' if live else '<span class="pill plan">Planned</span>'
        glyph = f' · diagram <span lang="zh-Hant">{c["diagram"]["glyph"]}</span>' if c.get("diagram", {}).get("glyph") else ""
        glyph = f' · {c["rank"]}{glyph}'
        inner = (f'<div class="top"><span class="num">{c["n"]}</span>{diagram(c)}</div>'
                 f'<div class="name"><h3>{c["rom"]}</h3><span class="ko">{c["ko"]}{glyph}</span></div>'
                 f'<p class="mean">{c["mean"]}</p><div class="foot"><span class="mv">{c["moves"]} movements</span>{pill}</div>')
        if not live and c.get("url"):
            inner += f'<a class="lib off" href="{esc(c["url"])}" target="_blank" rel="noopener">Official ITF page ↗</a>'
        out.append(f'<li><a class="card" href="/{c["slug"]}/" aria-label="Open {c["rom"]}">{inner}</a></li>' if live
                   else f'<li><div class="card soon">{inner}</div></li>')
    return "".join(out)

def refs(rows):
    return "".join(S.ref_card(r["kind"], r["icon"], r["src"], r["title"], r["desc"], r["url"]) for r in rows)

def forms_index():
    wl, wt, wbar = meter(WT)
    il, it, ibar = meter(ITF)
    body = f"""<header class="top">
  <div>
    <div class="eyebrow">Taekwondo forms · poomsae and tul</div>
    <h1>Forms <span>품새 · 틀</span></h1>
    <p class="lede">Two families of forms: the World Taekwondo forms set by the Kukkiwon (the eight Taegeuk and the black-belt poomsae), and the ITF patterns (Chang Hon tul). Every form gets the same treatment: the floor plan on its line, move-by-move cards on phones, the full sequence, and a two-page print sheet.</p>
    <p class="jump"><a href="#wt">World Taekwondo forms</a><a href="#itf">ITF forms</a></p>
  </div>
  <div class="status" aria-label="Progress">
    <div><small>World Taekwondo · published</small><b>{wl} / {wt}</b>{wbar}</div>
    <div><small>ITF · published</small><b>{il} / {it}</b>{ibar}</div>
  </div>
</header>
<section id="wt" class="family" aria-labelledby="wt-h"><h2 id="wt-h">World Taekwondo forms <span>Kukkiwon poomsae · 품새</span></h2>
  <p class="intro">The forms of World Taekwondo, as set and published by the Kukkiwon. Sequences and counts follow the Kukkiwon.</p>
  <h3 class="sub">Taegeuk <span>태극</span></h3><ul class="grid">{taegeuk_cards()}</ul>
  <h3 class="sub">Black-belt forms <span>유단자 품새</span></h3>
  <p class="intro">Yudanja poomsae, drawn the same way, each on its own floor line.</p>
  <ul class="bb">{bb_cards()}</ul>
  <div class="refs"><h3 class="sub">Official references</h3><ul>{refs(CAT["wtRefs"])}</ul></div></section>
<section id="itf" class="family" aria-labelledby="itf-h"><h2 id="itf-h">ITF forms <span>Chang Hon tul · 틀</span></h2>
  <p class="intro">The 24 patterns of the International Taekwon-Do Federation, devised by General Choi Hong Hi. Each pattern is performed on its own diagram, shown on each card from above with the ready position marked. Sequences and counts will follow the ITF Encyclopedia.</p>
  <h3 class="sub">Colour-belt patterns <span>gup</span></h3><ul class="grid">{itf_cards("gup")}</ul>
  <h3 class="sub">Black-belt patterns <span>dan</span></h3><ul class="grid">{itf_cards("dan")}</ul>
  <div class="refs"><h3 class="sub">Official references</h3><ul>{refs(CAT["itfRefs"])}</ul>
  <p class="intro note">There is more than one ITF. The card links go to the ITF led by Choi Jung Hwa, which publishes a page for every pattern (it calls pattern 15 Kodang). The Encyclopedia is published by the ITF in Vienna. See <a class="lib" href="/history/#itf-after">History</a> for how the federations came about.</p></div></section>
<section><p class="intro">New to the diagrams? <a class="lib" href="/how-to-read/">How to read a diagram</a> explains the floor line, the figures and the footprints. Every technique links to the <a class="lib" href="/library/">technique library</a>.</p></section>"""
    page("forms", "Forms · visualtkd", "Every taekwondo form on visualtkd: the World Taekwondo (Kukkiwon) poomsae, Taegeuk 1–8 and the black-belt forms, and the ITF patterns, with floor plans, move-by-move cards and print sheets.",
         body, FORMS_CSS + S.REF_CSS, active="forms")

# ---------------------------------------------------------------- landing (/)
def floor_svg():
    """The 王 floor line with Taegeuk Il Jang's path drawn on it (from its minimap positions)."""
    F = BY_SLUG.get("taegeuk/1")
    pts = [F["pos"][m["id"]] for m in F["moves"]] if F else []
    path = "M" + " L".join(f"{x} {y}" for x, y in pts) if pts else ""
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x, y in {tuple(p) for p in pts})
    return f"""<svg class="wang" viewBox="-6 -6 112 72" role="img" aria-label="The 王 floor line of Taegeuk Il Jang with the path of the form drawn on it">
  <path d="M4 8H96M4 30H96M4 52H96M50 8V52" class="ln"/>
  <path d="{path}" class="trail" pathLength="1"/>
  <g class="dots">{dots}</g>
  <circle cx="50" cy="8" r="3.2" class="start"/>
  <text x="50" y="1" text-anchor="middle">NA · 나</text><text x="50" y="63" text-anchor="middle">GA · 가</text>
</svg>"""

LANDING_CSS = """
.hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px 40px;align-items:center;padding-top:8px}
.hero h1{font-size:clamp(40px,6.4vw,68px)}
.hero .cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:15px;text-decoration:none;color:var(--ink);padding:10px 18px;border-radius:99px;border:1px solid var(--line);background:var(--surface)}
.btn:hover{border-color:var(--ink)}
.btn.primary{background:var(--ink);color:var(--surface);border-color:var(--ink)}
.btn:focus-visible{outline:2px solid var(--heaven);outline-offset:2px}
.board{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px}
.wang{width:100%;height:auto;display:block}
.wang .ln{stroke:var(--line);stroke-width:2.4;stroke-linecap:round;fill:none}
.wang .trail{stroke:var(--fire);stroke-width:1.1;fill:none;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 6s ease-in-out .4s forwards}
.wang .dots circle{fill:var(--heaven)}
.wang .start{fill:var(--fire)}
.wang text{font-family:var(--f-mono);font-size:3.6px;fill:var(--heaven);letter-spacing:.1em}
@keyframes draw{to{stroke-dashoffset:0}}
@media (prefers-reduced-motion:reduce){.wang .trail{animation:none;stroke-dashoffset:0}}
.board figcaption{font-size:12.5px;color:var(--muted);margin-top:8px}
.start3{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.start3 a{display:flex;flex-direction:column;gap:8px;height:100%;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:20px;color:inherit;text-decoration:none;transition:border-color .2s,transform .2s}
.start3 a:hover{border-color:var(--heaven);transform:translateY(-2px)}
.start3 a:focus-visible{outline:2px solid var(--heaven);outline-offset:3px}
.start3 .k{font-family:var(--f-mono);font-size:12px;letter-spacing:.1em;color:var(--fire);text-transform:uppercase}
.start3 h3{margin:0;font-family:var(--f-display);font-weight:700;font-size:22px}
.start3 h3 span{color:var(--muted);font-size:.7em;margin-left:.25em}
.start3 p{margin:0;color:var(--muted);font-size:14.5px}
.start3 .go{margin-top:auto;font-weight:600;font-size:14px;color:var(--heaven)}
.progress{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 24px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.progress b{font-family:var(--f-mono);font-weight:500;font-size:26px;font-variant-numeric:tabular-nums}
.progress small{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.meter{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:4px}
.meter i{height:8px;border-radius:3px;background:var(--line)}
.meter i.done{background:var(--fire)}
.progress p{grid-column:1/-1;margin:0;font-size:14px;color:var(--muted)}
.about{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px 36px}
.about h3{margin:0 0 6px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:600}
.about p{margin:0 0 10px;color:var(--muted);font-size:15px;max-width:60ch}
.about b{color:var(--ink);font-weight:600}
@media (max-width:760px){.hero{grid-template-columns:1fr}}
"""

def landing():
    live, total, bar = meter(WT)
    il, it, ibar = meter(ITF)
    ntech = sum(1 for k in LIB["techniques"] if appears("tech", k))
    nst = sum(1 for k, s in LIB["stances"].items() if "see" not in s)
    body = f"""<section class="hero">
  <div>
    <div class="eyebrow">Kukkiwon poomsae, drawn clearly</div>
    <h1>Every form, one move at a time</h1>
    <p class="lede">Modern diagrams of the taekwondo poomsae. Each form is laid out on its own floor line, steps through move by move on your phone, links every technique to a plain explanation, and prints as a two-page sheet for the dojang.</p>
    <div class="cta"><a class="btn primary" href="/forms/">Browse the forms</a><a class="btn" href="/taegeuk/1/">Start with Taegeuk Il Jang</a></div>
  </div>
  <figure class="board" style="margin:0">{floor_svg()}<figcaption>Taegeuk Il Jang on its 王 floor line: start at na, finish where you began.</figcaption></figure>
</section>

<section aria-labelledby="start"><h2 id="start">Start here</h2>
<ul class="start3">
  <li><a href="/forms/"><span class="k">{live + il} of {total + it} forms</span><h3>Forms <span>품새 · 틀</span></h3><p>The World Taekwondo forms, Taegeuk Il Jang to Pal Jang and the black-belt poomsae, each with its floor plan, move-by-move cards, full sequence and print sheet. The ITF patterns are next.</p><span class="go">All forms →</span></a></li>
  <li><a href="/library/"><span class="k">{nst} stances · {ntech} techniques</span><h3>Technique library <span>기술</span></h3><p>Every stance, block, strike and kick used in the forms: how it is done, the hand or foot surface it uses, and every move where it appears.</p><span class="go">Open the library →</span></a></li>
  <li><a href="/how-to-read/"><span class="k">Two-minute read</span><h3>How to read a diagram</h3><p>The floor line, which way the figures face, the footprints and stance chips, move numbers like 8-1 and 8-2, and how the print sheets work.</p><span class="go">Read the guide →</span></a></li>
</ul></section>

<section class="progress" aria-label="Progress">
  <div><small>World Taekwondo forms</small><b>{live} / {total}</b></div>{bar}
  <div><small>ITF forms</small><b>{il} / {it}</b></div>{ibar}
  <p>All {total} World Taekwondo forms are up: the eight Taegeuk and the nine black-belt poomsae. The {it} ITF patterns are planned; their diagrams are on the <a class="lib" href="/forms/#itf">forms page</a>.</p>
</section>

<section id="about" aria-labelledby="about-h"><h2 id="about-h">About</h2>
<div class="about">
  <div><h3>What this is</h3>
    <p>visualtkd is a study aid for the official taekwondo forms: the Kukkiwon poomsae of World Taekwondo now, and the ITF patterns next. The old book diagrams are hard to read on a phone and harder to teach from; these keep the original floor lines but redraw every move with a consistent figure, footprints and plain instructions.</p>
    <p>It is for students learning a form, and for instructors who want a clean sheet to hand out.</p></div>
  <div><h3>Sources</h3>
    <p>Sequences are checked against the <b>Kukkiwon</b> page for each form and at least one published move chart. Where sources disagree, or no source settles a detail, the choice is written down for review rather than decided silently.</p>
    <p>Every form page links to its official references. visualtkd is independent and is not affiliated with Kukkiwon, World Taekwondo or any ITF federation.</p></div>
  <div><h3>Print sheets and QR codes</h3>
    <p>Each form prints as two US Letter pages: the floor plan, then the full sequence and references. A QR code on each page opens the form on your phone, and every reference has its own short <b>visualtkd.com/go/</b> link, so printed sheets keep working even when a video or page moves.</p></div>
</div></section>"""
    page("", "visualtkd · Taekwondo poomsae, one move at a time",
         "Modern diagrams of the Kukkiwon taekwondo poomsae: floor plans, move-by-move cards for phones, a technique library and two-page print sheets.",
         body, LANDING_CSS, active=None)

# ---------------------------------------------------------------- how to read (/how-to-read/)
READ_CSS = """
.steps{display:flex;flex-direction:column;gap:18px;counter-reset:s}
.step{display:grid;grid-template-columns:minmax(0,400px) minmax(0,1fr);gap:20px 32px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px}
.step h2{font-size:22px}
.step h2::before{counter-increment:s;content:counter(s);display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--surface);font-family:var(--f-mono);font-size:14px;margin-right:10px;vertical-align:3px}
.step p{margin:0 0 10px;color:var(--muted);max-width:66ch}
.step p b{color:var(--ink);font-weight:600}
.step .art{background:var(--mat);border-radius:12px;padding:14px;display:flex;justify-content:center;align-items:center;gap:6px;min-height:180px;flex-wrap:wrap}
.step .art svg.body{height:160px;width:auto;overflow:visible}
.step .art .glow{display:none}
.wang{width:100%;height:auto}
.wang .ln{stroke:var(--ink);stroke-width:2;stroke-linecap:round;fill:none;opacity:.35}
.wang text{font-family:var(--f-mono);font-size:4.2px;fill:var(--heaven)}
.wang .you{fill:var(--fire)}
.fps{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:10px;width:100%}
.fps div{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:12.5px;text-align:center}
.fps svg{width:58px;height:58px}
.chips{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.chips div{display:flex;gap:10px;align-items:center;font-size:13.5px;color:var(--muted)}
#views{flex-wrap:nowrap}#views svg.body{height:135px}
.nums{font-family:var(--f-mono);font-size:14px;display:grid;grid-template-columns:auto 1fr;gap:6px 14px;align-items:baseline}
.nums b{color:var(--fire);font-weight:500}
.nums span{font-family:var(--f-body);color:var(--muted)}
@media (max-width:760px){.step{grid-template-columns:1fr}}
"""

def how_to_read():
    body = """<header><div class="eyebrow">Guide</div><h1>How to read a diagram</h1>
<p class="lede">Every form page uses the same conventions. Learn them once and every diagram on the site, and every print sheet, reads the same way.</p></header>
<div class="steps">

<section class="step"><div class="art"><svg class="wang" viewBox="-14 -8 128 76" role="img" aria-label="The 王 floor line with na at the top, ga at the bottom, ra on the left and da on the right">
  <path d="M4 8H96M4 30H96M4 52H96M50 8V52" class="ln"/>
  <text x="50" y="2" text-anchor="middle">NA · 나</text><text x="50" y="62" text-anchor="middle">GA · 가</text>
  <text x="-1" y="9.5" text-anchor="end">ra¹</text><text x="-1" y="31.5" text-anchor="end">ra²</text><text x="-1" y="53.5" text-anchor="end">ra³</text>
  <text x="101" y="9.5">da¹</text><text x="101" y="31.5">da²</text><text x="101" y="53.5">da³</text>
  <circle class="you" cx="50" cy="8" r="3"/><path d="M50 11v7" stroke="var(--fire)" stroke-width="1.6" stroke-linecap="round"/>
</svg></div>
<div><h2>The floor line</h2>
<p>Each form is performed along a fixed line, drawn as it appears in the Kukkiwon books. The Taegeuk forms use <b>王</b>: three bars joined by a centre line. The black-belt forms have their own shapes: 士 for Koryo, 山 for Keumgang, 工 for Taebaek.</p>
<p>You start at <b>na</b> (the top of the page) facing <b>ga</b> (the bottom). The bars are <b>ra</b> on the left of the page and <b>da</b> on the right, numbered 1–3 from the top. A left turn from the start faces da.</p></div></section>

<section class="step"><div class="art" id="views"></div>
<div><h2>Which way the figures face</h2>
<p>Figures on the left and right bars are drawn <b>from the side</b>, facing the way they move. Figures on the centre line face you when moving toward ga and show their <b>back</b> when returning toward na.</p>
<p><b>Near limbs are white, far limbs are grey.</b> That is how you tell the left arm or leg from the right. Horse- and crane-stance figures face the way the body faces, with the technique out to the side.</p></div></section>

<section class="step"><div class="art"><div class="fps" id="fps"></div></div>
<div><h2>Footprints</h2>
<p>The circle beside each figure is a top-down view of the feet, turned to the direction you face. The <b>red</b> foot leads (for crane stance, it is the standing foot), and the <b>blue tick</b> on the rim is the direction you face.</p>
<p>The shapes follow the stance: ap seogi short and almost in line, ap kubi long and a fist wide with the rear foot turned out, dwit kubi an L with the heels in line.</p></div></section>

<section class="step"><div class="art"><div class="chips" id="chips"></div></div>
<div><h2>Stance chips</h2>
<p>Under each figure, a chip names the stance and the leading foot: <b>L · Ap kubi</b> is a left front stance. Back stance is named by its <b>front</b> foot too, so L · Dwit kubi means the left foot is forward.</p>
<p>The chip style tells you the stance at a glance, even from across the room. On the form pages, chips and technique names link to the <a class="lib" href="/library/">technique library</a>.</p></div></section>

<section class="step"><div class="art"><div class="nums">
  <b>준비</b><span>Ready (junbi): the starting position</span>
  <b>7</b><span>One count, one figure</span>
  <b>8-1</b><span>A kick…</span>
  <b>8-2</b><span>…and the strike that lands with it share one number</span>
  <b>17-1 17-2</b><span>A block then a punch without stepping: one number, sub-counts</span>
  <b style="font-size:12px">기합 KIHAP</b><span>The shout, marked under the figure</span>
</div></div>
<div><h2>Move numbers</h2>
<p>Numbering follows the Kukkiwon count. When one step carries several techniques, each gets a sub-number, so every figure is exactly one count.</p>
<p>Punches are marked <b>bandae</b> when the punching hand matches the front foot, and <b>baro</b> when it is the opposite hand.</p></div></section>

<section class="step"><div class="art" id="phone"></div>
<div><h2>On your phone</h2>
<p>Phones show the form <b>move by move</b>: swipe or press Play. The small map in the corner of each card shows where you stand on the floor line and the path so far. Switch to <b>Floor plan</b> to see the whole form at once.</p>
<p>On a desktop, click any figure or table row to study it, and use the arrow keys to step through.</p></div></section>

<section class="step"><div class="art" style="flex-direction:column;align-items:flex-start;gap:8px;font-size:14px">
  <b>Page 1</b><span style="color:var(--muted)">Header, QR code and the whole floor plan, with a box for practice notes.</span>
  <b>Page 2</b><span style="color:var(--muted)">The full sequence table and the official references, each with its own QR code.</span></div>
<div><h2>Print sheets</h2>
<p>Every form has a two-page print sheet (the <b>Print sheet</b> button on its page). The QR code at the top right of each page opens the form on your phone.</p>
<p>References are printed as short links like <b>visualtkd.com/go/kukkiwon-t1</b>. If a video or page moves, the link is updated on the site, so old printouts keep working.</p></div></section>
</div>"""
    js = r"""
const V=[{id:"a",dir:"da1",view:"side",face:"R",stance:"front",lead:"L",arms:{L:"low"},tech:"low"},
         {id:"b",dir:"ga",view:"front",stance:"front",lead:"L",arms:{R:"punch"},tech:"punch"},
         {id:"c",dir:"na",view:"back",stance:"front",lead:"R",arms:{R:"punch"},tech:"punch"}];
const cap=["Side bar, facing da","Centre, toward ga","Centre, toward na"];
document.getElementById("views").innerHTML=V.map((m,i)=>`<div style="text-align:center;font-size:12px;color:var(--muted)">${figure(m)}<br>${cap[i]}</div>`).join("");
const F=[["walk","L","Ap seogi"],["front","L","Ap kubi"],["back","L","Dwit kubi"],["tiger","L","Beom seogi"],["horse",null,"Juchum seogi"],["crane","R","Hakdari seogi"],["kick","R","Ap chagi"]];
document.getElementById("fps").innerHTML=F.map(([s,l,n])=>`<div>${feet({dir:"na",stance:s,lead:l})}<a class="lib" href="${stanceHref(s)}">${n}</a></div>`).join("");
const C=[["walk","L","outlined"],["front","L","filled"],["back","L","double outline"],["tiger","L","dotted"],["horse",null,"shaded"],["crane","R","dotted blue"],["kick","R","dashed"]];
document.getElementById("chips").innerHTML=C.map(([s,l,d])=>`<div>${chip({stance:s,lead:l})}<span>${d}</span></div>`).join("");
document.getElementById("phone").innerHTML=`<div style="text-align:center">${figure({id:"p",dir:"da1",view:"side",face:"R",stance:"walk",lead:"R",arms:{R:"punch"},tech:"punch"})}${feet({dir:"da1",stance:"walk",lead:"R"})}</div>`;
document.querySelectorAll("#phone .fp,#views .fp").forEach(e=>{e.style.width="52px";e.style.height="52px"});
"""
    page("how-to-read", "How to read a diagram · visualtkd",
         "How the visualtkd poomsae diagrams work: the floor line, figure views, footprints, stance chips, move numbers and print sheets.",
         body, READ_CSS, js, active="how-to-read", figures=True)

# ---------------------------------------------------------------- library
LIB_CSS = """
.jump{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0;padding:0}
.jump a{display:inline-block;font-size:13.5px;font-weight:600;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:4px 12px}
.jump a:hover{border-color:var(--heaven);color:var(--heaven)}
.jump a:focus-visible{outline:2px solid var(--heaven);outline-offset:2px}
.group{margin:8px 0 -6px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}
.entries{display:flex;flex-direction:column;gap:16px}
.entry{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:20px 30px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px;scroll-margin-top:16px}
.entry:target{border-color:var(--fire);box-shadow:0 0 0 2px color-mix(in srgb,var(--fire) 25%,transparent)}
.entry .art{align-self:start;position:relative;background:var(--mat);--figbg:var(--mat);border-radius:12px;padding:12px 8px 6px;display:flex;justify-content:center;align-items:flex-end;gap:4px;min-height:210px}
.entry .art svg.body{height:200px;width:auto;max-width:48%;overflow:visible}
.entry .art .glow{display:none}
.entry .art .fp{position:absolute;right:8px;top:8px;width:54px;height:54px}
.entry .art figcaption{position:absolute;left:10px;top:8px;font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.entry h2{margin:0;font-size:26px}
.entry h2 .ko{word-break:keep-all;font-weight:700;color:var(--muted);font-size:.72em;margin-left:.25em}
.entry .en{margin:2px 0 12px;color:var(--muted);font-size:16px}
.entry p.desc{margin:0 0 12px;font-size:15.5px;max-width:66ch}
.facts{display:flex;flex-wrap:wrap;gap:8px 26px;margin:0 0 12px}
.facts div{display:flex;flex-direction:column}
.facts small{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
.facts b{font-weight:600;font-size:15px}
.points{margin:0 0 12px;padding-left:18px;color:var(--ink);font-size:14.5px}
.points li{margin:2px 0}
.where{font-size:14px;color:var(--muted)}
.where summary{cursor:pointer;font-weight:600;color:var(--ink);margin-bottom:6px}
.where summary:focus-visible{outline:2px solid var(--heaven);outline-offset:2px;border-radius:3px}
.where ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.where li b{color:var(--ink);font-weight:600;margin-right:6px}
.where a{font-family:var(--f-mono);font-size:12.5px;color:var(--heaven);text-decoration:none;padding:0 3px;border-radius:4px}
.where a:hover{background:var(--mat)}
.where a:focus-visible{outline:2px solid var(--heaven)}
.uses{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0;padding:0}
.uses a{font-size:13.5px}
.note{font-size:13px;color:var(--muted);border-left:3px solid var(--line);padding-left:12px;margin:0;max-width:72ch}
.fam{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.fam a{display:flex;flex-direction:column;gap:6px;height:100%;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 20px;color:inherit;text-decoration:none;transition:border-color .2s,transform .2s}
.fam a:hover{border-color:var(--heaven);transform:translateY(-2px)}
.fam a:focus-visible{outline:2px solid var(--heaven);outline-offset:3px}
.fam h3{margin:0;font-family:var(--f-display);font-weight:700;font-size:22px}
.fam h3 span{color:var(--muted);font-size:.7em;margin-left:.25em}
.fam .k{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;color:var(--fire)}
.fam p{margin:0;color:var(--muted);font-size:14px}
.find{display:flex;flex-direction:column;gap:10px}
.find input{font:inherit;font-size:16px;padding:10px 14px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);max-width:420px}
.find input:focus-visible{outline:2px solid var(--heaven);outline-offset:1px}
.az{list-style:none;margin:0;padding:0;columns:3 240px;column-gap:28px;font-size:14.5px}
.az li{break-inside:avoid;padding:3px 0}
.az .ko,.az .en{color:var(--muted);font-size:13px}
.az small{font-family:var(--f-mono);font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-left:4px}
@media (max-width:760px){.entry{grid-template-columns:1fr;padding:16px}.entry .art svg.body{height:180px}}
"""

def where_html(hits):
    if not hits:
        return '<p class="where">Not used in the forms built so far.</p>'
    n = sum(len(ids) for _, ids in hits)
    rows = "".join(
        f'<li><b>{esc(F["title"])}</b>' + " ".join(
            f'<a href="/{F["slug"]}/#move-{esc(i)}" aria-label="{esc(F["title"])} move {esc(i)}">{"준비" if i == "J" else esc(i)}</a>' for i in ids) + "</li>"
        for F, ids in hits)
    label = f'Appears in {len(hits)} form{"s" * (len(hits) != 1)} · {n} move{"s" * (n != 1)}'
    return f'<details class="where"{" open" if n <= 14 else ""}><summary>{label}</summary><ul>{rows}</ul></details>'

def art(moves, caption=""):
    """Placeholder figures (current renderer) filled in by figure.js in the browser."""
    data = esc(json.dumps(moves, ensure_ascii=False))
    cap = f"<figcaption>{esc(caption)}</figcaption>" if caption else ""
    return f'<figure class="art" data-moves="{data}" style="margin:0">{cap}</figure>'

FILL_JS = r"""
document.querySelectorAll(".art[data-moves]").forEach(el=>{
  const ms=JSON.parse(el.dataset.moves);
  el.insertAdjacentHTML("beforeend",ms.map(m=>figure(m)).join("")+(el.dataset.fp?feet({...ms[0],dir:"na"}):""));
});
document.querySelectorAll("[data-chip]").forEach(el=>{el.innerHTML=chip(JSON.parse(el.dataset.chip))});
"""

def lib_head(fam, extra=""):
    F = LIB["families"][fam]
    return (f'<header><div class="eyebrow"><a class="lib" href="/library/">Technique library</a> · {esc(F["rom"])}</div>'
            f'<h1>{esc(F["title"])} <span>{esc(F["ko"])}</span></h1><p class="lede">{esc(F["intro"])}</p>{extra}</header>')

def jump(items):
    return '<nav aria-label="On this page"><ul class="jump">' + "".join(
        f'<li><a href="#{esc(s)}">{esc(n)}</a></li>' for s, n in items) + "</ul></nav>"

def surface_link(key):
    if not key: return ""
    s = LIB["surfaces"][key]
    return f'<div><small>Surface</small><b><a class="lib" href="/library/hands-feet/#{s["slug"]}">{esc(s["en"])}</a> · {esc(s["ko"])}</b></div>'

def tech_entry(key):
    t = LIB["techniques"][key]
    m = demo("tech", key)
    facts = (f'<div><small>Height</small><b>{HEIGHT[t["height"]]}</b></div>' if t.get("height") else "") + surface_link(t.get("surface"))
    fig = art([m], f'{BY_FORM_MOVE[id(m)]} · move {m["id"]}') if m else ""
    if m: fig = fig.replace('class="art"', 'class="art" data-fp="1"', 1)
    return (f'<article class="entry" id="{t["slug"]}">{fig}<div>'
            f'<h2>{esc(t["name"])} <span class="ko">{t["ko"]}</span></h2><p class="en">{esc(t["en"])}</p>'
            f'<p class="desc">{esc(t["desc"])}</p>' + (f'<div class="facts">{facts}</div>' if facts else "")
            + where_html(appears("tech", key)) + "</div></article>")

BY_FORM_MOVE = {id(m): F["title"] for F in FORMS for m in F["moves"]}

def stance_entry(key):
    s = LIB["stances"][key]
    side, front = stance_demo(key, "side"), stance_demo(key, "front")
    fig = art([side, front], "side · front").replace('class="art"', 'class="art" data-fp="1"', 1)
    chip = esc(json.dumps({"stance": key, "lead": "R" if key == "crane" else "L"}))
    pts = "".join(f"<li>{esc(p)}</li>" for p in s.get("points", []))
    return (f'<article class="entry" id="{s["slug"]}">{fig}<div>'
            f'<h2>{esc(s["name"])} <span class="ko">{s["ko"]}</span></h2><p class="en">{esc(s["en"])}</p>'
            f'<p class="desc">{esc(s["desc"])}</p>' + (f'<ul class="points">{pts}</ul>' if pts else "")
            + f'<div class="facts"><div><small>Chip on the diagrams</small><b data-chip="{chip}"></b></div></div>'
            + where_html(appears("stance", key)) + "</div></article>")

def used_techs(fam):
    return [k for k, t in LIB["techniques"].items() if t["family"] == fam and appears("tech", k)]

def family_page(fam):
    if fam == "stances":
        sts = [k for k, s in LIB["stances"].items() if "see" not in s and appears("stance", k)]
        ready = used_techs("stances")
        items = [(LIB["stances"][k]["slug"], LIB["stances"][k]["name"]) for k in sts] + \
                [(LIB["techniques"][k]["slug"], LIB["techniques"][k]["name"]) for k in ready]
        body = (lib_head(fam) + jump(items) + '<div class="entries">' + "".join(stance_entry(k) for k in sts)
                + '<p class="group">Ready postures · 준비</p>' + "".join(tech_entry(k) for k in ready) + "</div>")
        count = len(sts) + len(ready)
    else:
        keys = used_techs(fam)
        groups = {}
        for k in keys: groups.setdefault(LIB["techniques"][k].get("group", ""), []).append(k)
        body = lib_head(fam) + jump([(LIB["techniques"][k]["slug"], LIB["techniques"][k]["name"]) for k in keys]) + '<div class="entries">'
        for g, ks in groups.items():
            if g: body += f'<p class="group">{esc(g)}</p>'
            body += "".join(tech_entry(k) for k in ks)
        body += "</div>"
        count = len(keys)
    body += '<p class="note">Figures are drawn with the current renderer from the first move in the forms that uses each technique. They will be redrawn with the new figure (character v2).</p>'
    F = LIB["families"][fam]
    page(f"library/{fam}", f'{F["title"]} · Technique library · visualtkd',
         f'{F["title"]} ({F["rom"]}) used in the Kukkiwon poomsae: how each is done and every move where it appears.',
         body, LIB_CSS, FILL_JS, active="library", figures=True)
    return count

def hands_feet_page():
    fam = "hands-feet"
    keys = [k for k in LIB["surfaces"] if surface_users(k)]
    parts = {"hand": "Hand", "arm": "Arm", "leg": "Leg", "foot": "Foot"}
    body = lib_head(fam) + jump([(LIB["surfaces"][k]["slug"], LIB["surfaces"][k]["en"]) for k in keys]) + '<div class="entries">'
    last = None
    for k in keys:
        s = LIB["surfaces"][k]
        if s["part"] != last:
            body += f'<p class="group">{parts[s["part"]]}</p>'; last = s["part"]
        users = surface_users(k)
        m = demo("tech", users[0])
        uses = "".join(f'<li><a class="lib" href="{S.tech_href(u)}">{esc(LIB["techniques"][u]["name"])}</a></li>' for u in users)
        body += (f'<article class="entry" id="{s["slug"]}">{art([m], "shown: " + LIB["techniques"][users[0]]["en"])}<div>'
                 f'<h2>{esc(s["name"])} <span class="ko">{s["ko"]}</span></h2><p class="en">{esc(s["en"])}</p>'
                 f'<p class="desc">{esc(s["desc"])}</p><div class="facts"><div><small>Used by</small></div></div>'
                 f'<ul class="uses">{uses}</ul></div></article>')
    body += ('</div><p class="note">Close-up drawings of each hand and foot surface come with the new figure (model sheet MS-8). '
             'Until then each entry shows a technique that uses it.</p>')
    F = LIB["families"][fam]
    page(f"library/{fam}", f'{F["title"]} · Technique library · visualtkd',
         "The striking and blocking surfaces of the hand, arm and foot used in the Kukkiwon poomsae.",
         body, LIB_CSS, FILL_JS, active="library", figures=True)
    return len(keys)

def library():
    counts = {f: (hands_feet_page() if f == "hands-feet" else family_page(f)) for f in S.FAMILIES}
    cards = "".join(
        f'<li><a href="/library/{f}/"><span class="k">{counts[f]} {"surfaces" if f == "hands-feet" else "entries"}</span>'
        f'<h3>{esc(F["title"])} <span>{esc(F["ko"])}</span></h3><p>{esc(F["intro"].split(". ")[0])}.</p></a></li>'
        for f, F in LIB["families"].items())
    az = []
    for k, s in LIB["stances"].items():
        if "see" not in s and appears("stance", k): az.append((s["name"], s["ko"], s["en"], f'/library/stances/#{s["slug"]}', "stance"))
    for k, t in LIB["techniques"].items():
        if appears("tech", k): az.append((t["name"], t["ko"], t["en"], S.tech_href(k), t["family"].rstrip("s")))
    for k in LIB["surfaces"]:
        s = LIB["surfaces"][k]
        if surface_users(k): az.append((s["name"], s["ko"], s["en"], f'/library/hands-feet/#{s["slug"]}', "surface"))
    az.sort(key=lambda r: r[0].lower())
    rows = "".join(f'<li data-q="{esc((n + " " + ko + " " + en).lower())}"><a class="lib" href="{h}">{esc(n)}</a> '
                   f'<span class="ko">{ko}</span> <span class="en">· {esc(en)}</span><small>{fam}</small></li>' for n, ko, en, h, fam in az)
    body = f"""<header><div class="eyebrow">Technique library · 기술</div><h1>Technique library</h1>
<p class="lede">Every stance and technique used in the forms on this site, explained in plain words, with the surface of the hand or foot it uses and a link to every move where it appears. The form pages link here from each technique name and stance chip.</p></header>
<ul class="fam">{cards}</ul>
<section class="find" aria-labelledby="az-h"><h2 id="az-h">A–Z</h2>
<label for="q" class="eyebrow" style="color:var(--muted)">Search in English, romanised Korean or Hangul</label>
<input id="q" type="search" placeholder="e.g. knife hand, makki, 앞굽이" autocomplete="off">
<ul class="az" id="az">{rows}</ul></section>"""
    js = r"""
const q=document.getElementById("q"),items=[...document.querySelectorAll("#az li")];
q.addEventListener("input",()=>{const v=q.value.trim().toLowerCase();items.forEach(li=>li.hidden=v&&!li.dataset.q.includes(v))});
"""
    page("library", "Technique library · visualtkd",
         "Stances, blocks, strikes, kicks and the hand and foot surfaces used in the Kukkiwon poomsae, each linked to every move where it appears.",
         body, LIB_CSS, js, active="library")

# ---------------------------------------------------------------- history (/history/)
HIST_CSS = """
.hist{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:28px 48px;align-items:start}
.hist article{display:flex;flex-direction:column;gap:30px;min-width:0}
.hist article section h2{scroll-margin-top:16px}
.hist article p{margin:0 0 12px;max-width:68ch;font-size:16px;line-height:1.6}
.hist article p b{font-weight:600}
.hist .yr{font-family:var(--f-mono);font-size:12px;letter-spacing:.1em;color:var(--fire);text-transform:uppercase;display:block;margin-bottom:4px}
.toc{position:sticky;top:16px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px}
.toc h2{font-size:13px;font-family:var(--f-body);letter-spacing:.14em;text-transform:uppercase;font-weight:600;margin:0 0 10px}
.toc ol{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;font-size:14.5px}
.tree{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;display:flex;flex-direction:column;align-items:center;gap:0}
.tree .node{border:1.5px solid var(--line);border-radius:10px;padding:8px 14px;text-align:center;background:var(--bg,transparent);max-width:100%;box-sizing:border-box}
.tree .node b{display:block;font-size:15px}
.tree .node span{display:block;font-size:12.5px;color:var(--muted)}
.tree .node.wt{border-color:var(--heaven)}.tree .node.wt b{color:var(--heaven)}
.tree .node.itf{border-color:var(--fire)}.tree .node.itf b{color:var(--fire)}
.tree .v{width:2px;height:18px;background:var(--line)}
.tree .split{display:grid;grid-template-columns:1fr 1fr;gap:0 18px;width:100%;position:relative;padding-top:18px}
.tree .split::before{content:"";position:absolute;top:0;left:25%;right:25%;height:2px;background:var(--line)}
.tree .lane{display:flex;flex-direction:column;align-items:center;position:relative}
.tree .lane::before{content:"";position:absolute;top:-18px;left:50%;width:2px;height:18px;background:var(--line)}
.tree .side{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:16px;padding-top:12px;border-top:1px dashed var(--line);width:100%}
.tree .side .node{border-style:dashed}
.tree figcaption{font-size:12.5px;color:var(--muted);margin-top:12px;text-align:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.two div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px}
.two h3{margin:0 0 6px;font-size:16px}
.two .wt h3{color:var(--heaven)}.two .itf h3{color:var(--fire)}
.two ul{margin:0;padding-left:18px;color:var(--muted);font-size:14.5px;display:flex;flex-direction:column;gap:4px}
.refs h2{margin-bottom:12px}
@media (max-width:900px){.hist{grid-template-columns:1fr}.toc{position:static;order:-1}}
@media (max-width:560px){.two{grid-template-columns:1fr}.tree{padding:14px 10px}.tree .split{gap:0 8px}.tree .node{padding:7px 8px}.tree .node b{font-size:13.5px}.tree .node span{font-size:11.5px}}
"""

HIST_REFS = [
    ("kuk", "gate", "Kukkiwon · Official site", "History of Taekwondo", "From subak and taekkyeon to the five kwans, the association and the Olympics.",
     "https://www.kukkiwon.or.kr/eng/contents/view?contentsNo=93&menuLevel=2&menuNo=94"),
    ("kuk", "gate", "Kukkiwon · Official site", "Kukkiwon chronology, 1970s", "The Central Dojang opening in 1972, the Kukkiwon name in 1973, the first dan certificates.",
     "https://www.kukkiwon.or.kr/eng/contents/view?contentsNo=101&menuLevel=3&menuNo=79"),
    ("kuk", "gate", "Kukkiwon · Official site", "Kukkiwon introduction", "What the Kukkiwon is: the World Taekwondo Headquarters, founded 30 November 1972.",
     "https://www.kukkiwon.or.kr/eng/contents/view?contentsNo=78&menuLevel=2&menuNo=80"),
    ("wt", "gate", "World Taekwondo · News", "WTF rebrands to World Taekwondo", "The new name and logo, announced in Muju on 23 June 2017.",
     "https://www.worldtaekwondo.org/news/NS/view?nid=29223"),
    ("itf", "gate", "ITF · Vienna · Official site", "History of Taekwon-Do", "The ITF's account: the 1955 name, the 1959 tour, the founding of the ITF in 1966.",
     "https://itf-tkd.org/history-of-taekwon%E2%80%91do/"),
    ("itf", "gate", "ITF · Choi Jung Hwa · Official site", "The 24 patterns", "One page per Chang Hon pattern.",
     "https://www.itf-administration.com/articles/?arturn=834"),
]

def history():
    toc = [("roots", "Roots, before 1945"), ("kwans", "The kwans, 1945–1955"), ("name", "One name: taekwondo"),
           ("itf", "The ITF and the Chang Hon patterns"), ("kukkiwon", "The Kukkiwon and the WTF"),
           ("wt", "From WTF to World Taekwondo"), ("itf-after", "The ITF after General Choi"),
           ("others", "Other branches"), ("forms", "Two families of forms")]
    body = f"""<header><div class="eyebrow">Background</div><h1>History <span>역사</span></h1>
<p class="lede">How a handful of schools opened in Seoul after 1945 became one martial art with two main branches, and why the forms on this site come in two sets: the World Taekwondo poomsae and the ITF patterns.</p></header>

<figure class="tree" style="margin:0" aria-label="Family tree of taekwondo">
  <div class="node"><b>Subak · taekkyeon · karate</b><span>older Korean traditions and arts learned under the occupation</span></div><div class="v"></div>
  <div class="node"><b>The five kwans</b><span>Seoul schools, from 1944–46</span></div><div class="v"></div>
  <div class="node"><b>Taekwondo</b><span>name chosen 1955 · Korea Taekwondo Association 1959</span></div>
  <div class="split">
    <div class="lane"><div class="node wt"><b>Kukkiwon</b><span>1972 · Seoul · curriculum and dan</span></div><div class="v"></div>
      <div class="node wt"><b>WTF</b><span>1973 · sport and competition</span></div><div class="v"></div>
      <div class="node wt"><b>World Taekwondo</b><span>renamed 2017 · Olympic sport</span></div></div>
    <div class="lane"><div class="node itf"><b>ITF</b><span>1966 · General Choi Hong Hi</span></div><div class="v"></div>
      <div class="node itf"><b>Toronto, then Vienna</b><span>headquarters from 1972</span></div><div class="v"></div>
      <div class="node itf"><b>Several ITFs</b><span>split 2001–2002</span></div></div>
  </div>
  <div class="side"><div class="node"><b>ATA</b><span>1969 · USA</span></div><div class="node"><b>GTF</b><span>1990</span></div><div class="node"><b>Independent kwans</b><span>tang soo do and others</span></div></div>
  <figcaption>Blue: the World Taekwondo branch, whose poomsae are on this site now. Red: the ITF branch, whose patterns are planned.</figcaption>
</figure>

<div class="hist">
<article>
<section id="roots"><h2>Roots, before 1945</h2>
  <p>Korea has a long record of fighting without weapons. Medieval chronicles describe <b>subak</b>, a bare-hand combat art practised by soldiers and ordinary people alike. Later came <b>kwonbeop</b>, a military fist art written into army manuals after the invasions of the late 1500s, and <b>taekkyeon</b>, a folk game of kicks and sweeps.</p>
  <p>During the Japanese occupation (1910–1945), judo and kendo were taught in Korea, and Koreans who studied in Japan or lived in Manchuria learned karate and Chinese boxing. Those arts shaped the first post-war schools far more directly than the older traditions did; the Korean kicking style came back into them over the following decades.</p></section>

<section id="kwans"><h2>The kwans, 1945–1955</h2>
  <p>After liberation, a handful of schools (<b>kwan</b>, 관) opened in and around Seoul. The five usually counted as the originals are <b>Chung Do Kwan</b>, <b>Moo Duk Kwan</b>, <b>Song Moo Kwan</b>, <b>Chang Moo Kwan</b> and <b>Ji Do Kwan</b> (first called Yun Moo Kwan). In the army, General <b>Choi Hong Hi</b> and Nam Tae Hi founded <b>Oh Do Kwan</b> in 1954.</p>
  <p>Each kwan taught under its own name (tang soo do, kong soo do, kwon bup) and mostly used karate kata as its forms. Over the years they added the higher, faster kicks that came to set the Korean art apart.</p></section>

<section id="name"><h2>One name: taekwondo</h2>
  <p><span class="yr">11 April 1955</span>A naming board of masters, historians and public figures chose <b>taekwondo</b> (태권도), the name General Choi submitted: <i>tae</i> foot, <i>kwon</i> fist, <i>do</i> way. Not every kwan used it at once.</p>
  <p><span class="yr">1959 – 1965</span>The <b>Korea Taekwondo Association</b> (KTA) was formed in 1959 with Choi as its first president. After a few years under another name, it settled as the single national body in the mid-1960s. Promotion tests were unified under it, and sparring became an event at the National Sports Festival in 1963.</p></section>

<section id="itf"><h2>The ITF and the Chang Hon patterns</h2>
  <p><span class="yr">22 March 1966</span>General Choi founded the <b>International Taekwon-Do Federation</b> (ITF) in Seoul, with member associations in nine countries, to spread the art abroad.</p>
  <p>He also built his own syllabus: the <b>Chang Hon</b> patterns (tul, 틀), named after his pen name. Each pattern is named after a person or event from Korean history, and its move count or diagram often carries a meaning (Yul-Gok has 38 moves for the 38th parallel, where the scholar Yi I was born). The set grew to <b>24 patterns</b>, one for each hour of the day, and was fixed in his 15-volume <i>Encyclopedia of Taekwon-Do</i> (1983). In the same years ITF technique settled on the rising-and-falling “sine wave” motion that marks the style today.</p>
  <p><span class="yr">1972</span>After falling out with the South Korean government, Choi moved to Canada and took the ITF headquarters to Toronto; it later moved to Vienna. His work with North Korea from 1980 onward widened the gap with Seoul.</p></section>

<section id="kukkiwon"><h2>The Kukkiwon and the WTF</h2>
  <p><span class="yr">1971 – 1973</span>In Seoul, the KTA under <b>Kim Un-yong</b> built a central training hall. It opened on <b>30 November 1972</b> and was named the <b>Kukkiwon</b> (국기원, “house of the national martial art”) in February 1973. From December 1973, dan certificates were issued in the Kukkiwon president's name.</p>
  <p>The association also set new forms for the whole country: the eight <b>Taegeuk</b> poomsae for coloured belts and the black-belt poomsae from Koryo to Ilyeo. These replaced the earlier Palgwe forms and the karate kata the kwans had used. The kwans themselves were formally merged in 1978.</p>
  <p><span class="yr">28 May 1973</span>Three days after the first World Taekwondo Championships opened at the Kukkiwon, delegates founded the <b>World Taekwondo Federation</b> (WTF) there, with Kim Un-yong as president.</p>
  <p>The two bodies split the work. The <b>Kukkiwon</b> is the World Taekwondo Headquarters: it keeps the curriculum and the poomsae, trains instructors and issues dan and poom certificates worldwide. The <b>WTF</b> is the sport's international federation: competition rules, championships and the Olympics. That is why the same style is called “Kukkiwon taekwondo”, “WT style” or “Olympic style”: the poomsae come from the Kukkiwon, the competition from the WTF.</p></section>

<section id="wt"><h2>From WTF to World Taekwondo</h2>
  <p><span class="yr">1988 – 2000</span>Taekwondo was a demonstration sport at the Seoul 1988 and Barcelona 1992 Olympics and became a full medal sport at Sydney 2000, under WTF rules. Poomsae has its own world championships, judged under World Taekwondo's poomsae rules.</p>
  <p><span class="yr">23 June 2017</span>At its General Assembly in Muju, the WTF renamed itself <b>World Taekwondo</b> (WT), mainly because “WTF” had taken on an unwanted meaning online. It is the same body; only the name changed. The Kukkiwon is still the headquarters for the art, and its poomsae are the forms on this site's World Taekwondo section.</p></section>

<section id="itf-after"><h2>The ITF after General Choi</h2>
  <p>General Choi died in Pyongyang in 2002. A dispute over his succession, which had begun the year before, left several federations each calling itself the ITF. The two largest today are the ITF based in <b>Vienna</b>, which publishes the Encyclopedia, and the ITF led by his son <b>Choi Jung Hwa</b>.</p>
  <p>All of them teach the Chang Hon patterns, with small differences. The best known is pattern 15: the original <b>Ko-Dang</b> was replaced by <b>Juche</b> in the 1980s, and federations still differ on which name, and which sequence, they use.</p>
  <p>Since 2014 the Vienna ITF and World Taekwondo have signed an agreement to cooperate and have given joint demonstrations.</p></section>

<section id="others"><h2>Other branches</h2>
  <p>Some masters went their own way. The <b>American Taekwondo Association</b> (ATA), founded in the United States in 1969, teaches its own Songahm forms. The <b>Global Taekwondo Federation</b> (GTF), founded in 1990 by a former ITF master, keeps Ko-Dang and adds patterns of its own. Many independent schools still teach the kwan-era forms under names such as tang soo do.</p></section>

<section id="forms"><h2>Two families of forms</h2>
  <p>So a student today usually learns one of two sets of forms. This site covers both.</p>
  <div class="two">
    <div class="wt"><h3>World Taekwondo · poomsae 품새</h3><ul>
      <li>Set by the Kukkiwon; used by World Taekwondo schools and in Olympic-style clubs</li>
      <li>8 Taegeuk forms for coloured belts, 9 black-belt forms</li>
      <li>Front stance is <i>ap kubi</i>; counted by Kukkiwon move numbers</li>
      <li><a class="lib" href="/forms/#wt">All 17 on this site</a></li></ul></div>
    <div class="itf"><h3>ITF · tul 틀</h3><ul>
      <li>Devised by General Choi; used by ITF schools</li>
      <li>24 patterns from Chon-Ji to Tong-Il, each on its own diagram</li>
      <li>Front stance is <i>gunnun sogi</i>; sine-wave motion</li>
      <li><a class="lib" href="/forms/#itf">Planned on this site</a></li></ul></div>
  </div></section>

<section class="refs" aria-labelledby="src-h"><h2 id="src-h">Official references</h2><ul>{"".join(S.ref_card(*r) for r in HIST_REFS)}</ul>
  <p class="intro" style="margin-top:12px">Accounts of the early kwan years differ between sources, and each federation tells its own history. This page keeps to dates the official sources agree on and describes the rest in our own words.</p></section>
</article>
<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{"".join(f'<li><a class="lib" href="#{k}">{t}</a></li>' for k, t in toc)}</ol></nav>
</div>"""
    page("history", "History of taekwondo · visualtkd",
         "A short history of taekwondo: the kwans, the name in 1955, the ITF and its Chang Hon patterns, the Kukkiwon and the WTF, and how the WTF became World Taekwondo.",
         body, HIST_CSS + S.REF_CSS, active="history")

if __name__ == "__main__":
    landing(); forms_index(); history(); how_to_read(); library()
