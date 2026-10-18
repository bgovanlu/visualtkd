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

def lib_js():
    """What the figure renderer needs in the browser: names and library links, nothing else."""
    t = {k: [v["name"], v["ko"], v["en"], tech_href(k)] for k, v in LIB["techniques"].items()}
    s = {k: stance_names(k) + [stance_href(k)] for k in LIB["stances"]}
    return json.dumps({"t": t, "s": s}, ensure_ascii=False).replace("</", "<\\/")

def form_files():
    """forms/*.json in teaching order: Taegeuk 1-8, the black-belt forms, then the ITF patterns, in catalogue order."""
    order = [f["slug"] for f in CATALOG["taegeuk"] + CATALOG["blackbelt"] + CATALOG.get("itf", [])]
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
NAV = [("forms", "/forms/", "Forms"), ("library", "/library/", "Library"),
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
