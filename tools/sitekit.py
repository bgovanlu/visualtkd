"""sitekit: shared pieces for tools/build_form.py and tools/build_site.py: the technique library data,
the forms catalogue, the site nav and footer, and the inlined CSS/JS every page carries."""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://visualtkd.com"

def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()

def load(rel):
    return json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))

LIB = load("data/techniques.json")
CATALOG = load("data/catalog.json")
FAMILIES = list(LIB["families"])          # stances, blocks, strikes, kicks, hands-feet

def tech_href(key):
    t = LIB["techniques"][key]
    return f'/library/{t["family"]}/#{t["slug"]}'

def stance_href(key):
    s = LIB["stances"][key]
    return tech_href(s["see"]) if "see" in s else f'/library/stances/#{s["slug"]}'

def stance_names(key):
    """[romanised, Hangul, English] for a stance key; kicking 'stances' borrow the kick's name."""
    s = LIB["stances"][key]
    if "see" in s:
        t = LIB["techniques"][s["see"]]
        return [t["name"], t["ko"], "Knee strike" if key == "knee" else "Kicking"]
    return [s["name"], s["ko"], s["en"]]

def lib_js(itf=False):
    """What the figure renderer needs in the browser: names and library links, nothing else.
    itf: ITF forms use each entry's ITF names (`itf` in data/techniques.json) where it has them."""
    nm = lambda v: v.get("itf", v) if itf else v
    t = {k: [nm(v)["name"], nm(v)["ko"], nm(v)["en"], tech_href(k)] for k, v in LIB["techniques"].items()}
    s = {k: ([nm(LIB["stances"][k])[f] for f in ("name", "ko", "en")] if itf and "itf" in LIB["stances"][k] else stance_names(k))
            + [stance_href(k)] for k in LIB["stances"]}
    return json.dumps({"t": t, "s": s}, ensure_ascii=False).replace("</", "<\\/")

def form_files():
    """forms/*.json in teaching order: the basic forms, Taegeuk 1-8, the black-belt forms, then the ITF patterns, in catalogue order."""
    order = [f["slug"] for f in CATALOG.get("kicho", []) + CATALOG["taegeuk"] + CATALOG["blackbelt"] + CATALOG.get("itf", [])]
    files = {}
    for name in os.listdir(os.path.join(ROOT, "forms")):
        if name.endswith(".json"):
            F = load(f"forms/{name}")
            files[F["slug"]] = os.path.join(ROOT, "forms", name)
    unknown = set(files) - set(order)
    assert not unknown, f"forms missing from data/catalog.json: {unknown}"
    return [files[s] for s in order if s in files]

BRAND = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="5" fill="var(--heaven)"/>'
         '<path d="M5 6h14M6.5 12h11M5 18h14M12 6v12" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>')
NAV = [("forms", "/forms/", "Forms"), ("library", "/library/", "Library"), ("history", "/history/", "History"),
       ("how-to-read", "/how-to-read/", "How to read"), ("about", "/#about", "About")]

def nav(active=None):
    items = "".join(f'<li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
                    for key, href, label in NAV)
    return (f'<nav class="sitenav" aria-label="Site"><a class="brand" href="/">{BRAND}visualtkd</a>'
            f'<ul>{items}</ul></nav>')

def footer(extra=""):
    return ('<footer class="sitefoot"><p>World Taekwondo form names, sequences and counts follow Kukkiwon; ITF patterns follow the ITF Encyclopedia of Taekwon-Do. '
            'Descriptions are our own words; see each form&rsquo;s official references for the source text.'
            f'{(" " + extra) if extra else ""}</p><p><a href="/">visualtkd.com</a></p></footer>')

def esc(s):
    return html.escape(str(s), quote=True)

# Reference cards: a generic icon per kind of source (gate = official site, play = video,
# channel, document = PDF); never a brand logo. Form pages and the site pages share these.
REF_ICON = {
 "gate": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 7.5c3 .9 6 1.3 9.5 1.3s6.5-.4 9.5-1.3M4 10.5h16M6 10.5V20M18 10.5V20M10 10.5V20M14 10.5V20M4.5 20h15M7.5 8.6 6.4 5.8M16.5 8.6l1.1-2.8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "play": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10 8.3v7.4l6-3.7z" fill="currentColor"/></svg>',
 "channel": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="13" rx="3" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10.2 8.6v5.8l4.8-2.9z" fill="currentColor"/><path d="M7 21h10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "pdf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2.8h8.4L19 7.4v13.8H6z M14.2 2.8v4.8H19" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><text x="12.4" y="17.6" font-size="5.6" font-weight="700" text-anchor="middle" fill="currentColor" font-family="IBM Plex Sans Condensed,Arial,sans-serif">PDF</text></svg>',
}

REF_CSS = """
.refs ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:10px}
.ref{display:flex;gap:14px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px;color:inherit;text-decoration:none;height:100%;box-sizing:border-box;transition:border-color .2s}
.ref:hover{border-color:var(--ico)}
.ref:focus-visible{outline:2px solid var(--heaven);outline-offset:2px}
.ref.kuk{--ico:var(--heaven)}.ref.yt{--ico:var(--fire)}.ref.wt{--ico:var(--ink)}.ref.itf{--ico:var(--fire)}
.ico{flex:none;width:46px;height:46px;border-radius:12px;display:grid;place-items:center;color:var(--ico);background:color-mix(in srgb,var(--ico) 11%,transparent)}
.ico svg{width:28px;height:28px}
.rt{display:flex;flex-direction:column;gap:2px;min-width:0}
.rt small{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ico)}
.rt b{font-size:15.5px;line-height:1.25}
.rt b::after{content:" \\2197";font-size:12px;color:var(--muted)}
.rt span{font-size:13px;color:var(--muted)}
"""

def ref_card(kind, icon, src, title, desc, url):
    """One reference link for the site pages (form pages build theirs in build_form.refs)."""
    return (f'<li><a class="ref {kind}" href="{esc(url)}" target="_blank" rel="noopener">'
            f'<span class="ico">{REF_ICON[icon]}</span><span class="rt"><small>{src}</small><b>{title}</b>'
            f'<span>{desc}</span></span></a></li>')
