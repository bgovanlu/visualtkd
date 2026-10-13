"""Generate form pages from templates/form.html + forms/<form>.json.

usage:
  python3 tools/build_form.py forms/taegeuk-2.json            # page only
  python3 tools/build_form.py forms/taegeuk-2.json --print    # page + print PDF + QR check
  python3 tools/build_form.py --all --print                   # every form

Also regenerates site/_redirects from the refs of every form, so the /go/
short links used by printed QR codes always cover every published sheet.
"""
import glob, html, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://visualtkd.com"

ICON = {
 "gate": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 7.5c3 .9 6 1.3 9.5 1.3s6.5-.4 9.5-1.3M4 10.5h16M6 10.5V20M18 10.5V20M10 10.5V20M14 10.5V20M4.5 20h15M7.5 8.6 6.4 5.8M16.5 8.6l1.1-2.8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "play": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10 8.3v7.4l6-3.7z" fill="currentColor"/></svg>',
 "channel": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="13" rx="3" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10.2 8.6v5.8l4.8-2.9z" fill="currentColor"/><path d="M7 21h10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "pdf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2.8h8.4L19 7.4v13.8H6z M14.2 2.8v4.8H19" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><text x="12.4" y="17.6" font-size="5.6" font-weight="700" text-anchor="middle" fill="currentColor" font-family="IBM Plex Sans Condensed,Arial,sans-serif">PDF</text></svg>',
}

def tri(t):
    bars = "".join('<i></i>' if l else '<i class="brk"><s></s><s></s></i>' for l in t["lines"])
    return f'<div class="tri" aria-label="{t["name"]} trigram {t["sym"]}">{bars}</div>'

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
        assert m["dir"] in ("na","ga","da1","da2","da3","ra1","ra2","ra3"), m
        if m["view"] == "side": assert m.get("face") in ("L","R"), m

def build(path, do_print):
    F = json.load(open(path))
    check(F)
    t = open(os.path.join(ROOT, "templates/form.html")).read()
    data = json.dumps({k: F[k] for k in ("moves","layout","pos")}, ensure_ascii=False).replace("</", "<\\/")
    tg = F["trigram"]
    rep = {
        "TITLE": F["title"], "KO": F["ko"], "PDF": F["pdf"], "BOARD_MIN": str(F["boardMin"]),
        "TRI": tri(tg), "TRIGRAM": f'{tg["name"]} {tg["sym"]} · {tg["meaning"]}',
        "MOVEMENTS": str(F["movements"]), "COUNTS": str(len(F["moves"]) - 1),
        "NOTE_H": F["note"]["h"], "NOTE_P": F["note"]["p"], "REFS": refs(F), "FOOTER": F["footer"], "FORM_JSON": data,
    }
    for k, v in rep.items(): t = t.replace("{{" + k + "}}", v)
    assert "{{" not in t, "unfilled placeholder"
    out_dir = os.path.join(ROOT, "site", F["slug"]); os.makedirs(out_dir, exist_ok=True)
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
    files = sorted(glob.glob(os.path.join(ROOT, "forms/*.json"))) if "--all" in sys.argv else args
    for f in files: build(f, "--print" in sys.argv)
    redirects()
