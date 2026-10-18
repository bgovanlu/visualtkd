"""Screenshot the site pages through a local server (absolute links work) and report script errors
and horizontal overflow on a phone.

usage: python3 tools/check/pages.py [path ...]     (default: the landing, forms, how-to-read and library pages)
       -> shots/page-<name>-desk.png, shots/page-<name>-phone.png
"""
import functools, http.server, os, sys, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "shots"); os.makedirs(OUT, exist_ok=True)
paths = sys.argv[1:] or ["/", "/forms/", "/history/", "/how-to-read/", "/library/", "/library/stances/", "/library/blocks/",
                         "/library/strikes/", "/library/kicks/", "/library/hands-feet/"]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Quiet, directory=os.path.join(ROOT, "site"))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"
with sync_playwright() as p:
    br = p.chromium.launch()
    for mode, vp, dsf in (("desk", {"width": 1300, "height": 900}, 1), ("phone", {"width": 390, "height": 844}, 2)):
        pg = br.new_page(viewport=vp, device_scale_factor=dsf)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        for path in paths:
            errs.clear(); pg.goto(base + path); pg.wait_for_timeout(700)
            name = path.strip("/").replace("/", "-").replace("#", "_") or "home"
            pg.screenshot(path=f"{OUT}/page-{name}-{mode}.png", full_page=True)
            w = pg.evaluate("document.documentElement.scrollWidth")
            print(f"{mode:5} {path:24} width {w}{'  OVERFLOW' if w > vp['width'] else ''}  errors: {errs or 'none'}")
        pg.close()
    br.close()
srv.shutdown()
