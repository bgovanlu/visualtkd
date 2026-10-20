"""botkit: shared pieces for tools/bot/fix_issues.py and tools/bot/ship.py: paths, gh calls and the
owner check that every label-driven step goes through (anyone can open an issue on the public repo,
but only the owner's labels move work along)."""
import fcntl, json, os, subprocess, sys

REPO = "bgovanlu/visualtkd"
OWNER = "bgovanlu"
GIT_URL = f"git@github.com:{REPO}.git"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # Brian's checkout: .venv and tools/node_modules live here
DATA = os.path.expanduser("~/.local/share/visualtkd-bot")   # bare clone, work clones, deploy clone
STATE = os.path.expanduser("~/.local/state/visualtkd-bot")  # state files and per-run logs
PROTECTED = ("tools/bot/", ".github/", "infra/", "tools/deploy_aws.py", "CLAUDE.md", ".claude/",
             "tools/requirements.txt", "tools/package.json", "tools/package-lock.json")

def run(cmd, **kw):
    kw.setdefault("check", True)
    return subprocess.run(cmd, text=True, capture_output=True, **kw)

def git(*args, cwd, check=True):
    return run(["git", *args], cwd=cwd, check=check).stdout.strip()

def gh(*args, check=True):
    return run(["gh", *args], check=check).stdout

def gh_json(*args):
    return json.loads(gh(*args) or "null")

def labelled_by(number, label):
    """Login of whoever last added `label` to issue/PR `number` (None if it was never added)."""
    events = gh_json("api", "--paginate", "--slurp", f"repos/{REPO}/issues/{number}/events")
    who = None
    for page in events:
        for e in page:
            if e.get("event") == "labeled" and e.get("label", {}).get("name") == label:
                who = e["actor"]["login"]
    return who

def protected(paths):
    return [p for p in paths if p.startswith(PROTECTED)]

def lock(name):
    """Hold an exclusive lock for the life of the process; exit quietly if another run has it."""
    os.makedirs(STATE, exist_ok=True)
    f = open(os.path.join(STATE, f"{name}.lock"), "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"{name}: another run is in progress"); sys.exit(0)
    return f

def load_state(name, default):
    try:
        return json.load(open(os.path.join(STATE, f"{name}.json")))
    except FileNotFoundError:
        return default

def save_state(name, data):
    path = os.path.join(STATE, f"{name}.json")
    json.dump(data, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)

def bare():
    """The bot's bare clone, with main brought up to date from GitHub."""
    path = os.path.join(DATA, "base.git")
    if not os.path.isdir(path):
        os.makedirs(DATA, exist_ok=True)
        run(["git", "clone", "-q", "--bare", ROOT, path])
        git("remote", "set-url", "origin", GIT_URL, cwd=path)
    git("fetch", "-q", "origin", "+main:main", cwd=path)
    return path
