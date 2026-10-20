"""Ship what Brian approved, with no LLM in the loop: merge every open PR he has labelled `ship`,
then deploy main to AWS (tools/deploy_aws.py, full deploy so /go/ links follow) whenever a PR
labelled `ship` or `bot-pr` has been merged since the last deploy. Comments the deploy on each PR.

usage: python3 tools/bot/ship.py [--dry-run]
Run every 15 minutes by tools/bot/systemd/visualtkd-ship.timer. The first run only records the PRs
already merged, so nothing old is redeployed.
"""
import argparse, datetime, os, sys
import botkit as B

SHIP, OPENED = "ship", "bot-pr"

def merge_approved(dry):
    for p in B.gh_json("pr", "list", "-R", B.REPO, "--label", SHIP, "--state", "open", "--json", "number,isDraft,baseRefName"):
        n = p["number"]
        if p["isDraft"] or p["baseRefName"] != "main":
            continue
        who = B.labelled_by(n, SHIP)
        if who != B.OWNER:
            print(f"PR #{n}: `{SHIP}` was added by {who}, not {B.OWNER}; ignored"); continue
        if dry:
            print(f"PR #{n}: would merge"); continue
        r = B.run(["gh", "pr", "merge", str(n), "-R", B.REPO, "--squash", "--delete-branch"], check=False)
        if r.returncode:
            print(f"PR #{n}: merge failed: {r.stderr.strip()}", file=sys.stderr)
            B.gh("pr", "edit", str(n), "-R", B.REPO, "--remove-label", SHIP)
            B.gh("pr", "comment", str(n), "-R", B.REPO, "--body",
                 "🤖 **Shipper:** couldn't merge this (conflict or failing checks), so I removed `ship`. "
                 "Rebase or fix it, then add `ship` again.")
        else:
            print(f"PR #{n}: merged")

def merged_since_last(state):
    seen = set(state["shipped"])
    prs = {}
    for label in (SHIP, OPENED):
        for p in B.gh_json("pr", "list", "-R", B.REPO, "--label", label, "--state", "merged", "--json", "number,mergedBy", "--limit", "100"):
            prs[p["number"]] = p
    return [n for n, p in sorted(prs.items()) if n not in seen and (p.get("mergedBy") or {}).get("login") == B.OWNER]

def deploy(prs, state, dry):
    clone = os.path.join(B.DATA, "deploy")
    if not os.path.isdir(clone):
        B.run(["git", "clone", "-q", B.bare(), clone])
    B.git("fetch", "-q", B.bare(), "main", cwd=clone)
    B.git("checkout", "-q", "--detach", "FETCH_HEAD", cwd=clone)
    sha = B.git("rev-parse", "--short", "HEAD", cwd=clone)
    print(f"deploying main {sha} for PR(s) {prs}", flush=True)
    if dry:
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    log = os.path.join(B.STATE, "runs", f"{stamp}-deploy-{sha}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    r = B.run([sys.executable, os.path.join(clone, "tools/deploy_aws.py")], cwd=clone, check=False)
    open(log, "w").write(r.stdout + r.stderr)
    ok = r.returncode == 0
    msg = (f"🤖 **Shipper:** deployed `main` at {sha} to https://visualtkd.com." if ok else
           f"🤖 **Shipper:** deploy of `main` at {sha} **failed**; log on the dev box: `{log}`. "
           "It is retried every 15 minutes.")
    if ok or state.get("failed") != sha:          # a failing deploy is reported once, not every 15 minutes
        for n in prs:
            B.gh("pr", "comment", str(n), "-R", B.REPO, "--body", msg)
    if ok:
        state["shipped"] += prs
        state["deployed"] = sha
    state["failed"] = None if ok else sha
    B.save_state("ship", state)
    print("deployed" if ok else f"deploy failed, see {log}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    _lock = B.lock("ship")
    state = B.load_state("ship", None)
    if state is None:
        state = {"shipped": [], "deployed": None}
        state["shipped"] = merged_since_last(state)
        B.save_state("ship", state)
        print(f"first run: recorded {len(state['shipped'])} already-merged PR(s); nothing deployed")
        return
    merge_approved(a.dry_run)
    prs = merged_since_last(state)
    if prs:
        deploy(prs, state, a.dry_run)

if __name__ == "__main__":
    main()
