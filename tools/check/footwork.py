"""Run the floor simulator (templates/footwork.js) on every form under Node and report where each
form ends relative to its start, plus every count's footwork.

usage: python3 tools/check/footwork.py            # summary: drift per form
       python3 tools/check/footwork.py taegeuk-1  # every count of one form

Kukkiwon forms finish where they started (the final baro step brings the feet back to the ready
position), so a large drift means the simulator, or the move data, puts a step in the wrong place.
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import sitekit as S

JS = r"""
const FW=require(process.argv[1]);const forms=JSON.parse(require('fs').readFileSync(0,'utf8'));
const out={};for(const [k,M] of Object.entries(forms))out[k]=FW.simulate(M);
process.stdout.write(JSON.stringify(out));
"""

def run(files):
    forms = {os.path.basename(p)[:-5]: json.load(open(p))["moves"] for p in files}
    res = subprocess.run(["node", "-e", JS, os.path.join(ROOT, "templates/footwork.js")], input=json.dumps(forms),
                         capture_output=True, text=True, check=True)
    return forms, json.loads(res.stdout)

if __name__ == "__main__":
    files = S.form_files()
    if len(sys.argv) > 1: files = [p for p in files if os.path.basename(p)[:-5] in sys.argv[1:]]
    forms, sim = run(files)
    for k, R in sim.items():
        c = lambda f: ((f["L"]["p"][0] + f["R"]["p"][0]) / 2, (f["L"]["p"][1] + f["R"]["p"][1]) / 2)
        s, e = c(R[0]["feet"]), c(R[-1]["feet"])
        xs = [p for r in R for f in ("L", "R") for p in [r["feet"][f]["p"][0]]]
        ys = [p for r in R for f in ("L", "R") for p in [r["feet"][f]["p"][1]]]
        print(f"{k:11} ends {((e[0]-s[0])**2+(e[1]-s[1])**2)**.5:5.1f} ft-lengths from the start  "
              f"(end x {e[0]:+5.1f} y {e[1]:+5.1f})  floor {max(xs)-min(xs):4.1f} wide x {max(ys)-min(ys):4.1f} deep")
        if len(sys.argv) > 1:
            for m, r in zip(forms[k], R):
                f = r["feet"]
                print(f'   {m["id"]:5} {m["dir"]:4} {m["stance"]:6} {m.get("lead") or "-"}  {r["how"]:15} moved {",".join(r["moved"]) or "-":4}'
                      f'  L({f["L"]["p"][0]:+5.1f},{f["L"]["p"][1]:+5.1f}){"*" if f["L"].get("air") else " "}'
                      f'  R({f["R"]["p"][0]:+5.1f},{f["R"]["p"][1]:+5.1f}){"*" if f["R"].get("air") else " "}  {m["desc"][:60]}')
