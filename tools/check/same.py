"""Screenshot the same-stance treatments (issue #4) side by side for review.

usage: python3 tools/check/same.py taegeuk/8 [a b c]  -> shots/same-<slug>-<mode>-board.png (+ -phone.png)
"""
import functools, http.server, os, sys, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "shots"); os.makedirs(OUT, exist_ok=True)
slug, modes = sys.argv[1], sys.argv[2:] or ["off", "a", "b", "c"]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=os.path.join(ROOT, "site")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}/{slug}/"
name = slug.replace("/", "-")
with sync_playwright() as p:
    br = p.chromium.launch()
    for mode in modes:
        pg = br.new_page(viewport={"width": 1900, "height": 1200}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"{base}?same={mode}"); pg.wait_for_timeout(1000)
        pg.locator(".scroller").screenshot(path=f"{OUT}/same-{name}-{mode}-board.png")
        print(mode, "board width", pg.evaluate("document.querySelector('.board').scrollWidth"), "errors:", errs or "none")
        ph = br.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        # open the phone carousel on the first count that carries its stance
        first = pg.evaluate("(()=>{const b=[...document.querySelectorAll('.fig')].find(x=>x.querySelector('.same')||x.dataset.g);"
                            "return b?(b.dataset.g?b.dataset.g.split(' ').pop():b.dataset.i):null})()")
        mid = pg.evaluate(f"document.querySelectorAll('#rows tr')[{first}].cells[0].textContent") if first is not None else ""
        ph.goto(f"{base}?same={mode}#move-{mid}"); ph.wait_for_timeout(1200)
        ph.locator(".carousel").screenshot(path=f"{OUT}/same-{name}-{mode}-phone.png")
        pg.close(); ph.close()
    br.close()
srv.shutdown()
