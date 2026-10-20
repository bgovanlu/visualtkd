"""Work the issues Brian has triaged: every open issue labelled `bot-ready` (by the owner) gets an
unattended Claude Code run in its own clone, sandboxed (tools/bot/sandbox.json: no credentials, no
sockets, no network except the official form sources), then this wrapper pushes the branch and
opens a PR labelled `bot-pr`. Claude never pushes, never touches gh and never sees AWS.

usage: python3 tools/bot/fix_issues.py [--max N] [--issue N] [--dry-run]
Run every 4 hours by tools/bot/systemd/visualtkd-fix.timer; logs in ~/.local/state/visualtkd-bot/runs/.
"""
import argparse, datetime, json, os, shutil, subprocess, sys
import botkit as B

READY, OPENED, QUESTION, FAILED = "bot-ready", "bot-pr", "bot-question", "bot-failed"
TIMEOUT = 75 * 60
CLEAN_ENV = ("SSH_AUTH_SOCK", "DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR", "GH_TOKEN", "GITHUB_TOKEN",
             "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_PROFILE",
             "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "GPG_AGENT_INFO")
FOOTER = ("\n\n---\nOpened by the dev-box fixer (`tools/bot/fix_issues.py`). To ship it, add the `ship` label "
          "(the shipper merges and deploys within 15 minutes) or merge it yourself (deployed on the next pass)."
          "\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)")

def issue_text(n):
    I = B.gh_json("issue", "view", str(n), "-R", B.REPO, "--json", "title,body,author,comments,url")
    parts = [f"# #{n}: {I['title']}", f"Opened by @{I['author']['login']} · {I['url']}", "", I["body"] or "(no body)"]
    for c in I["comments"]:
        parts += ["", f"## Comment by @{c['author']['login']}", "", c["body"]]
    return "\n".join(parts)

def relabel(n, add, comment=None):
    B.gh("issue", "edit", str(n), "-R", B.REPO, "--remove-label", READY, "--add-label", add)
    if comment:
        B.gh("issue", "comment", str(n), "-R", B.REPO, "--body", comment)

def work(n, log, dry):
    branch = f"bot/issue-{n}"
    wt = os.path.join(B.DATA, "work", f"issue-{n}")
    shutil.rmtree(wt, ignore_errors=True)
    os.makedirs(os.path.dirname(wt), exist_ok=True)
    B.run(["git", "clone", "-q", "--local", "-b", "main", B.bare(), wt])
    B.git("remote", "set-url", "origin", B.GIT_URL, cwd=wt)
    B.git("checkout", "-q", "-b", branch, cwd=wt)
    os.symlink(os.path.join(B.ROOT, ".venv"), os.path.join(wt, ".venv"))
    os.symlink(os.path.join(B.ROOT, "tools/node_modules"), os.path.join(wt, "tools/node_modules"))
    with open(os.path.join(wt, ".git/info/exclude"), "a") as f:
        f.write("\n.venv\ntools/node_modules\n.bot/\n")
    os.makedirs(os.path.join(wt, ".bot"))
    open(os.path.join(wt, ".bot/issue.md"), "w").write(issue_text(n))
    base = B.git("rev-parse", "HEAD", cwd=wt)

    prompt = open(os.path.join(B.HERE, "fix_prompt.md")).read().format(number=n)
    env = {k: v for k, v in os.environ.items() if k not in CLEAN_ENV}
    cmd = ["claude", "-p", prompt, "--settings", os.path.join(B.HERE, "sandbox.json"), "--setting-sources", "user",
           "--permission-mode", "dontAsk", "--model", "opus", "--max-turns", "250",
           "--allowedTools", "Read", "Edit", "Write", "Glob", "Grep", "Bash", "TodoWrite", "Agent",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           "--output-format", "json", "--no-session-persistence"]
    print(f"#{n}: running Claude in {wt}", flush=True)
    try:
        p = subprocess.run(cmd, cwd=wt, env=env, text=True, capture_output=True, timeout=TIMEOUT, stdin=subprocess.DEVNULL)
        out = p.stdout
    except subprocess.TimeoutExpired as e:
        out = f"timeout after {TIMEOUT}s\n{e.stdout or ''}"
    open(log, "w").write(out)

    try:
        R = json.load(open(os.path.join(wt, ".bot/result.json")))
        status = R["status"]
    except (OSError, ValueError, KeyError, TypeError):
        R, status = {}, None
    print(f"#{n}: result {status}", flush=True)
    if dry:
        print(json.dumps(R, indent=1)); return

    if status == "skip":
        relabel(n, FAILED)
        print(f"#{n}: skipped: {R.get('reason', '')}")
    elif status == "question":
        relabel(n, QUESTION, "🤖 **Dev-box fixer:** I didn't change anything yet.\n\n" + R["comment"][:6000])
    elif status == "pr":
        commits = int(B.git("rev-list", "--count", f"{base}..HEAD", cwd=wt))
        files = B.git("diff", "--name-only", f"{base}...HEAD", cwd=wt).splitlines()
        bad = B.protected(files)
        if not commits or bad:
            why = f"it changed protected files ({', '.join(bad)})" if bad else "it reported a fix but made no commit"
            relabel(n, FAILED, f"🤖 **Dev-box fixer:** no PR opened: {why}. Details in the run log on the dev box.")
            return
        B.git("push", "-q", "-f", "origin", branch, cwd=wt)
        body = R["body"][:50000].replace("🤖 Generated with [Claude Code](https://claude.com/claude-code)", "").rstrip()
        body += f"\n\nFixes #{n}" + FOOTER
        url = B.gh("pr", "create", "-R", B.REPO, "--base", "main", "--head", branch,
                   "--title", R["title"][:200], "--body", body, "--label", OPENED).strip()
        relabel(n, OPENED, f"🤖 **Dev-box fixer:** proposed fix in {url}")
        print(f"#{n}: opened {url}")
    else:
        relabel(n, FAILED, "🤖 **Dev-box fixer:** the run ended without a result. Details in the run log on the dev box; "
                           "add `bot-ready` again to retry.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=3, help="issues per run")
    ap.add_argument("--issue", type=int, help="work this issue only (it must still be labelled bot-ready)")
    ap.add_argument("--dry-run", action="store_true", help="run Claude but don't push, open PRs or relabel")
    a = ap.parse_args()
    _lock = B.lock("fix")
    issues = B.gh_json("issue", "list", "-R", B.REPO, "--label", READY, "--state", "open", "--json", "number", "--limit", "50")
    todo = sorted(i["number"] for i in issues if a.issue in (None, i["number"]))
    runs = os.path.join(B.STATE, "runs"); os.makedirs(runs, exist_ok=True)
    done = 0
    for n in todo:
        if done >= a.max:
            break
        who = B.labelled_by(n, READY)
        if who != B.OWNER:
            print(f"#{n}: `{READY}` was added by {who}, not {B.OWNER}; ignored"); continue
        if B.gh_json("pr", "list", "-R", B.REPO, "--head", f"bot/issue-{n}", "--state", "open", "--json", "number"):
            print(f"#{n}: a bot PR is already open"); continue
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        try:
            work(n, os.path.join(runs, f"{stamp}-issue-{n}.json"), a.dry_run)
        except Exception as e:
            print(f"#{n}: error: {e!r}", file=sys.stderr)
        done += 1
    print(f"fix: {done} issue(s) worked, {len(todo)} labelled {READY}")

if __name__ == "__main__":
    main()
