"""Render a pose-guide image of the 3D mannequin for every distinct pose.

usage: python3 tools/poses/render.py [out_dir] [--only id1,id2]
Reads data/poses.json (+ data/pose-overrides.json) and writes <out_dir>/<pose-id>/mannequin.png
(default out_dir: design/models/v4). Each image uses the view and facing the pose is drawn in.
"""
import json, os, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = os.path.join(ROOT, args[0] if args else "design/models/v4")
    only = None
    if "--only" in sys.argv: only = set(sys.argv[sys.argv.index("--only")+1].split(","))
    poses = json.load(open(os.path.join(ROOT, "data/poses.json")))["poses"]
    try: ovr = json.load(open(os.path.join(ROOT, "data/pose-overrides.json")))
    except FileNotFoundError: ovr = {}
    srv = serve(); url = f"http://127.0.0.1:{srv.server_address[1]}/tools/poses/mannequin.html?render"
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pg = b.new_page(viewport={"width": 768, "height": 1152})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(url)
        try: pg.wait_for_function("window.ready === true", timeout=20000)
        except Exception: raise SystemExit("mannequin page failed to load: " + "; ".join(errs))
        n = 0
        for po in poses:
            if only and po["id"] not in only: continue
            spec = {"stance": po["stance"], "lead": po["lead"], "arms": po["arms"]}
            d = os.path.join(out, po["id"]); os.makedirs(d, exist_ok=True)
            views = [(po["view"], po["face"] or "R", "mannequin.png")]
            if "--all-views" in sys.argv:   # for checking: every angle plus the top view
                views += [("front","R","front.png"),("side","R","side-R.png"),("back","R","back.png"),("top","R","top.png")]
            for v, f, name in views:
                pg.evaluate("([s,o,v,f]) => window.renderPose(s,o,v,f)", [spec, ovr.get(po["id"], {}), v, f])
                pg.locator("#c").screenshot(path=os.path.join(d, name))
            n += 1
        b.close()
    srv.shutdown()
    print(f"{n} pose guides -> {os.path.relpath(out, ROOT)}", "errors: " + "; ".join(errs) if errs else "")

if __name__ == "__main__":
    main()
