"""Build the 2-page print PDF for one form page.

usage: python3 tools/build_print.py site/taegeuk/1/index.html site/taegeuk/1/taegeuk-1-print.pdf \
         https://visualtkd.com/taegeuk/1 "Taegeuk Il Jang" "태극 1장 · 18 movements"
Page 1: header + floor plan.  Page 2: full sequence + references.
Both pages carry a QR to the form's page on the site; every reference gets its own QR.
A running footer names where the sheet was printed from, the edition and page x of y.
"""
import os, re, sys, html, datetime
import qrcode, qrcode.image.svg
from playwright.sync_api import sync_playwright

src, out, site, title, korean = sys.argv[1:6]
D = os.path.dirname(os.path.abspath(src))
s = open(src).read()

def qr_svg(url, label):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(url); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    d = "".join(f"M{x} {y}h1v1h-1z" for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (f'<svg class="qr" viewBox="-2 -2 {n+4} {n+4}" shape-rendering="crispEdges" role="img" aria-label="QR code: {html.escape(label)}">'
            f'<rect x="-2" y="-2" width="{n+4}" height="{n+4}" fill="#fff"/><path d="{d}" fill="#000"/></svg>')

short = re.sub(r"^https?://", "", site).rstrip("/")
form_qr = qr_svg(site, short)

# one QR per reference card, matched by order of the .ref anchors
ref_urls = ["https://visualtkd.com/go/" + g for g in re.findall(r"<a data-go=\"([^\"]+)\" class=\"ref ", s)]
ref_qrs = [qr_svg(u, u) for u in ref_urls]

FP = "file://" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules/@fontsource")
css = f"""<style>
@font-face{{font-family:"IBM Plex Sans Condensed";font-weight:400;src:url("{FP}/ibm-plex-sans-condensed/files/ibm-plex-sans-condensed-latin-400-normal.woff2")}}
@font-face{{font-family:"IBM Plex Sans Condensed";font-weight:600;src:url("{FP}/ibm-plex-sans-condensed/files/ibm-plex-sans-condensed-latin-600-normal.woff2")}}
@font-face{{font-family:"IBM Plex Sans Condensed";font-weight:700;src:url("{FP}/ibm-plex-sans-condensed/files/ibm-plex-sans-condensed-latin-700-normal.woff2")}}
@font-face{{font-family:"IBM Plex Mono";font-weight:500;src:url("{FP}/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2")}}
:root{{--f-display:"Noto Serif CJK KR",serif;--f-body:"IBM Plex Sans Condensed","Noto Sans CJK KR",sans-serif}}
*{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{background:#fff}}
.wrap{{max-width:none;padding:0;gap:14px}}
.actions,.mtoggle,.carousel,.study,footer,header .meta,.sitenav,.fwsec{{display:none!important}}
a.lib{{text-decoration:none}}
.scroller{{overflow:visible}}
.fig .glow{{display:none}}
.seq{{break-before:page}}
table{{min-width:0}} th,td{{padding:6px 10px}} tr.on td{{background:none}}
body.dense th,body.dense td{{padding:2px 10px;line-height:1.3}} body.dense .ref .qr{{width:100px;height:100px}}
.ruled{{display:flex;flex-direction:column;gap:22px;margin-top:6px}}
.ruled i{{display:block;border-bottom:1px solid var(--line);width:240px}}
/* form QR block, top right of both pages */
.scan{{display:flex;align-items:center;gap:12px}}
.scan .qr{{width:112px;height:112px}}
.scan p{{margin:0;font-size:13px;color:var(--muted);line-height:1.35;max-width:150px}}
.scan b{{display:block;color:var(--ink);font-size:14px}}
.scan code{{font-family:var(--f-mono);font-size:11.5px;color:var(--ink)}}
.p2head{{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:12px}}
.p2head h2{{margin:0;font-family:var(--f-display);font-weight:700;font-size:26px;line-height:1.15}}
.p2head h2 small{{display:block;font-family:var(--f-body);font-weight:400;font-size:14px;color:var(--muted)}}
.seq > h2{{display:none}}
/* references with QR */
.refs{{break-inside:avoid;margin-top:4px}}
.refs h2{{font-size:20px;margin-bottom:8px}}
.refs ul{{grid-template-columns:repeat(3,1fr);gap:8px}}
.ref{{padding:10px;gap:10px;align-items:center}}
.ref .ico{{width:34px;height:34px;border-radius:9px}} .ref .ico svg{{width:21px;height:21px}}
.ref .qr{{flex:none;width:118px;height:118px;margin-left:auto}}
.rt b{{font-size:14px}} .rt span{{font-size:12px}}
.rt em{{display:block}}
.rt b::after{{content:""}}
</style>"""

js = f"""<script>
document.documentElement.dataset.theme="light";
const FORM_QR={form_qr!r};
const REF_QRS={ref_qrs!r};
addEventListener("load",()=>{{
  document.querySelectorAll(".fig.on").forEach(e=>e.classList.remove("on"));
  // site links would print as dead file:// links: keep the text, drop the link
  document.querySelectorAll("a.lib").forEach(e=>e.removeAttribute("href"));
  const n=document.getElementById("nBelt");
  n.innerHTML='<h3>Practice notes</h3><div class="ruled"><i></i><i></i><i></i><i></i></div>';
  const scan=`<div class="scan">${{FORM_QR}}<p><b>Scan to practise</b>Step-by-step on your phone<br><code>{short}</code></p></div>`;
  document.querySelector("header").insertAdjacentHTML("beforeend",scan);
  document.querySelector(".seq").insertAdjacentHTML("afterbegin",
    `<div class="p2head"><h2>{html.escape(title)} · Full sequence<small>{html.escape(korean)}</small></h2>${{scan}}</div>`);
  document.querySelectorAll(".ref").forEach((a,i)=>{{if(REF_QRS[i])a.insertAdjacentHTML("beforeend",REF_QRS[i])}});
}});
</script>"""

if "</body>" in s:   # a full site page
    page = s.replace("</body>", css + js + "</body>")
else:                # a bare page fragment
    page = ('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width"></head>'
            '<body style="margin:0">' + s + css + js + '</body></html>')
tmp = os.path.join(D, "_print_" + os.path.basename(src))
open(tmp, "w").write(page)

edition = datetime.date.today().strftime("%B %Y")
footer = f"""<div style="width:100%;margin:0 0.4in;padding-top:5px;border-top:0.5pt solid #c3cbd8;display:flex;justify-content:space-between;
 font-family:'IBM Plex Sans Condensed','Noto Sans CJK KR',sans-serif;font-size:7.5pt;color:#5a6377">
 <span>Printed from <b style="color:#141a2b">{short}</b> · {html.escape(title)} {html.escape(korean)}</span>
 <span>Edition {edition} · Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>"""

with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1180, "height": 1400})
    pg.goto("file://" + tmp); pg.wait_for_timeout(900)
    # wider forms need a wider layout before measuring
    bw = pg.evaluate("document.querySelector('.board').scrollWidth")
    if bw + 40 > 1180:
        pg.set_viewport_size({"width": bw + 40, "height": 1400}); pg.wait_for_timeout(300)
    # page 1 ends after the board, or after the notes box when a form moves its notes under the board
    h1 = pg.evaluate("""(()=>{const n=document.getElementById('notes'),b=(n&&!n.hidden?n:document.querySelector('.scroller'));
      return b.getBoundingClientRect().bottom - document.querySelector('header').getBoundingClientRect().top})()""")
    w = pg.evaluate("document.querySelector('.wrap').scrollWidth")
    avail_w, avail_h = 7.7 * 96, (11 - 0.4 - 0.65) * 96
    scale = round(min(avail_w / w, (avail_h - 10) / h1) - 0.004, 3)
    # Wide boards shrink everything; zoom page 2 back up so the sequence table stays readable
    # (target: the type size of Taegeuk 8, scale ~0.54), as far as it still fits on one page.
    k = round(0.54 / scale, 2)
    if k < 1.1: k = 1.0          # Taegeuk-sized sheets print as they are
    if k > 1.0: pg.evaluate("document.body.classList.add('dense')")   # long forms: tighter table rows
    while k > 1.0:
        pg.evaluate(f"document.querySelectorAll('.seq,.refs').forEach(e=>e.style.zoom={k})")
        h2 = pg.evaluate("document.querySelector('.refs').getBoundingClientRect().bottom - document.querySelector('.seq').getBoundingClientRect().top")
        if h2 * scale <= avail_h - 12: break
        k = round(k - 0.05, 2)
    if k <= 1.0: pg.evaluate("document.querySelectorAll('.seq,.refs').forEach(e=>e.style.zoom='')")
    print(f"page-2 zoom {k}")
    pg.pdf(path=out, format="Letter", scale=scale, print_background=True,
           margin={"top": "0.4in", "bottom": "0.65in", "left": "0.4in", "right": "0.4in"},
           display_header_footer=True, header_template="<div></div>", footer_template=footer)
    br.close()
os.remove(tmp)
print(f"scale {scale}  page1 {h1:.0f}px  refs {len(ref_urls)}  -> {out}")
