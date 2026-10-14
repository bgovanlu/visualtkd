"""Screenshot a built form page for review.

usage:
  python3 tools/check/shot.py koryo            # desktop floor plan (+ notes box) -> shots/
  python3 tools/check/shot.py taegeuk/7 phone  # phone carousel card; prints page width (must be 390)
"""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "shots"); os.makedirs(OUT, exist_ok=True)
slug = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else "desk"; name = slug.replace("/", "-")
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1900, "height": 1200}) if mode == "desk" else \
         br.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"file://{ROOT}/site/{slug}/index.html"); pg.wait_for_timeout(1200)
    if mode == "desk":
        pg.locator(".scroller").screenshot(path=f"{OUT}/{name}-board.png")
        if pg.locator("#notes").is_visible(): pg.locator("#notes").screenshot(path=f"{OUT}/{name}-notes.png")
        print("board width", pg.evaluate("document.querySelector('.board').scrollWidth"))
    else:
        pg.screenshot(path=f"{OUT}/{name}-phone.png")
        print("page width", pg.evaluate("document.documentElement.scrollWidth"), "(390 = no horizontal scroll)")
    print("script errors:", errs or "none")
    br.close()
