"""Generate form pages from templates/form.html + forms/<form>.json.

usage:
  python3 tools/build_form.py forms/taegeuk-2.json            # page only
  python3 tools/build_form.py forms/taegeuk-2.json --print    # page + print PDF + QR check
  python3 tools/build_form.py --all --print                   # every form
  python3 tools/build_form.py forms/taegeuk-1.json --images   # per-move images from design/moves/ -> preview/ (never deployed)

Also regenerates site/_redirects from the refs of every form, so the /go/
short links used by printed QR codes always cover every published sheet.
"""
import glob, html, json, os, subprocess, sys
import sitekit as S
from sitekit import ROOT, SITE

ICON = S.REF_ICON

def tri(t):
    bars = "".join('<i></i>' if l else '<i class="brk"><s></s><s></s></i>' for l in t["lines"])
    return f'<div class="tri" aria-label="{t["name"]} trigram {t["sym"]}">{bars}</div>'

def seal(sym):
    """Black-belt forms: the name in Hanja, set as a vertical seal, instead of a trigram."""
    return f'<div class="seal" lang="zh-Hant" aria-label="{sym["name"]} {sym["hanja"]}">{sym["hanja"]}</div>'

def refs(F):
    out = ""
    for r in F["refs"]:
        out += (f'      <li><a data-go="{r["go"]}" class="ref {r["kind"]}" href="{html.escape(r["url"])}" target="_blank" rel="noopener">'
                f'<span class="ico">{ICON[r["icon"]]}</span><span class="rt"><small>{r["src"]}</small><b>{r["title"]}</b>'
                f'<span>{r["desc"]}</span><em>visualtkd.com/go/{r["go"]}</em></span></a></li>\n')
    return out

def check(F):
    ids = [m["id"] for m in F["moves"]]
    assert len(ids) == len(set(ids)), "duplicate move ids"
    placed = []
    for k, row in F["layout"].items():
        for x in row: placed += x if isinstance(x, list) else [x]
    missing, extra = set(ids) - set(placed), set(placed) - set(ids)
    assert not missing and not extra, f"layout mismatch: missing {missing} extra {extra}"
    assert set(F["pos"]) == set(ids), f"minimap positions missing for {set(ids) - set(F['pos'])}"
    for m in F["moves"]:
        # every technique and stance must have a library entry (data/techniques.json)
        assert m["tech"] in S.LIB["techniques"], f'move {m["id"]}: no library entry for technique "{m["tech"]}"'
        assert m["stance"] in S.LIB["stances"], f'move {m["id"]}: no library entry for stance "{m["stance"]}"'
        assert m["dir"] in ("na","ga","na4","na5","ga4","ga5","da1","da2","da3","ra1","ra2","ra3","gada","nada","gara","nara"), m
        if m["view"] == "side": assert m.get("face") in ("L","R"), m

def build(path, do_print, images=False):
    F = json.load(open(path))
    check(F)
    t = open(os.path.join(ROOT, "templates/form.html")).read()
    data = json.dumps({k: F[k] for k in ("moves","layout","pos","floor","family") if k in F}, ensure_ascii=False).replace("</", "<\\/")
    if "trigram" in F:      # Taegeuk: trigram bars + "Geon ☰ · Heaven"
        tg = F["trigram"]; mark, line = tri(tg), f'{tg["name"]} {tg["sym"]} · {tg["meaning"]}'
    else:                   # black-belt forms: Hanja seal + "高麗 · Goryeo, the scholar-warrior"
        sym = F["symbol"]; mark, line = seal(sym), f'{sym["hanja"]} · {sym["meaning"]}'
    rep = {
        "TITLE": F["title"], "KO": F["ko"], "PDF": F["pdf"], "BOARD_MIN": str(F["boardMin"]),
        "TRI": mark, "TRIGRAM": line, "GLYPH": F.get("floor", {}).get("glyph", "王"),
        "MOVEMENTS": str(F["movements"]), "COUNTS": str(len(F["moves"]) - 1),
        # big forms shrink the cards so every bar fits: optional cardW / figH in the JSON
        "SIZE_CSS": f':root{{--card-w:{F["cardW"]}px;--fig-h:{F["figH"]}px}}' if "cardW" in F else "",
        "BASE_CSS": S.read("templates/base.css"), "NAV": S.nav("forms"), "SITEFOOT": S.footer(),
        "FIGURE_JS": S.read("templates/figure.js"), "LIB_JSON": S.lib_js(F.get("family") == "itf"),
        "FOOTWORK_JS": S.read("templates/footwork.js").replace("if(typeof module", "if(false&&typeof module"),
        "NOTE_H": F["note"]["h"], "NOTE_P": F["note"]["p"], "REFS": refs(F), "FOOTER": F["footer"], "FORM_JSON": data,
    }
    # --images: figures from design/moves/<form>/ (tools/figures.py), built into preview/ until they are approved
    out_dir = os.path.join(ROOT, "preview" if images else "site", F["slug"]); os.makedirs(out_dir, exist_ok=True)
    if images:
        import figures
        stem = os.path.splitext(os.path.basename(path))[0]
        rep["FIGURE_JS"] = "const FIGIMG=" + json.dumps(figures.build(stem, F, out_dir)) + ";\n" + rep["FIGURE_JS"]
    for k, v in rep.items(): t = t.replace("{{" + k + "}}", v)
    assert "{{" not in t, "unfilled placeholder"

    page = os.path.join(out_dir, "index.html"); open(page, "w").write(t)
    print("page ->", os.path.relpath(page, ROOT))
    if do_print:
        pdf = os.path.join(out_dir, F["pdf"])
        subprocess.check_call([sys.executable, os.path.join(ROOT, "tools/build_print.py"), page, pdf,
                               f'{SITE}/{F["slug"]}', F["title"], f'{F["ko"]} · {F["movements"]} movements'])
        verify(pdf, [f'{SITE}/{F["slug"]}'] + [f'{SITE}/go/{r["go"]}' for r in F["refs"]])

def verify(pdf, expected):
    """Decode every QR code in the finished PDF and compare with what should be there."""
    import tempfile, zxingcpp
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(["pdftoppm", "-r", "300", "-png", pdf, os.path.join(d, "p")])
        found = []
        for png in sorted(glob.glob(os.path.join(d, "p*.png"))):
            found += [r.text for r in zxingcpp.read_barcodes(Image.open(png))]
    need = expected + [expected[0]]          # the form QR is on both pages
    assert sorted(found) == sorted(need), f"QR mismatch\n found {sorted(found)}\n need  {sorted(need)}"
    print(f"QR ok: {len(found)} codes decode to the expected links")

def redirects():
    seen = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "forms/*.json"))):
        for r in json.load(open(p))["refs"]:
            if seen.setdefault(r["go"], r["url"]) != r["url"]:
                raise SystemExit(f'/go/{r["go"]} points to two different URLs')
    body = "".join(f"/go/{k:<20} {v}  302\n" for k, v in seen.items())
    open(os.path.join(ROOT, "site/_redirects"), "w").write(
        "# visualtkd.com short links used by printed QR codes (generated by tools/build_form.py)\n"
        "# 302 so a destination can change without stale browser caches\n" + body)
    print(f"_redirects -> {len(seen)} links")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = S.form_files() if "--all" in sys.argv else args
    for f in files: build(f, "--print" in sys.argv, "--images" in sys.argv)
    if "--images" in sys.argv: sys.exit()     # a preview: leave site/ alone
    redirects()
    # landing, forms index, how-to-read and the library list every form and move: keep them in step
    subprocess.check_call([sys.executable, os.path.join(ROOT, "tools/build_site.py")])
