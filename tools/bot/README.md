# Dev-box bot

Site feedback becomes a deployed fix with two approvals from Brian and no LLM near the credentials.

1. **Feedback.** The Feedback button on every page opens the GitHub issue form (`.github/ISSUE_TEMPLATE/feedback.yml`); the issue gets `feedback`.
2. **Triage (Brian).** Add `bot-ready` to an issue the bot may work on. Labels added by anyone else are ignored.
3. **Fix, every 4 hours** (`fix_issues.py`, `visualtkd-fix.timer`). Each `bot-ready` issue (3 per run, oldest first) gets its own clone under `~/.local/share/visualtkd-bot/work/` and an unattended `claude -p` run with `fix_prompt.md`, sandboxed by `sandbox.json`: no `~/.aws`, `~/.ssh`, gh or keyring access, no sockets under `/run/user`, no internet except WebFetch to the official form sources, writes only inside the clone. Claude commits locally and writes `.bot/result.json`; the wrapper then
   - `pr`: pushes `bot/issue-<n>` and opens a PR labelled `bot-pr` (refused if it touches `tools/bot/`, `.github/`, `infra/`, `tools/deploy_aws.py`, `CLAUDE.md` or the dependency files); the issue moves to `bot-pr`;
   - `question`: comments on the issue and labels it `bot-question` (sources don't settle it, or it needs a decision);
   - anything else: labels it `bot-failed`. Add `bot-ready` again to retry.
4. **Approve (Brian).** GitHub won't let you approve a PR opened under your own account, so approval is the `ship` label, or merging it yourself.
5. **Ship, every 15 minutes** (`ship.py`, `visualtkd-ship.timer`). Merges (squash) every open PR the owner labelled `ship`, then, if any `ship` or `bot-pr` PR was merged by the owner since the last deploy, runs `tools/deploy_aws.py` from a clean clone of `main` and comments the result on each PR.

```
tools/bot/install.sh                                   # install / refresh the timers
systemctl --user list-timers 'visualtkd-*'
journalctl --user -u visualtkd-fix -u visualtkd-ship -e
python3 tools/bot/fix_issues.py --issue 42 --dry-run   # one issue, no push / PR / labels
systemctl --user start visualtkd-fix                   # run now
```

Run logs (Claude's JSON output with cost, deploy output): `~/.local/state/visualtkd-bot/runs/`. Shipper state: `~/.local/state/visualtkd-bot/ship.json`.

Claude runs on the dev box's logged-in subscription (`~/.claude/.credentials.json`); if runs start failing with auth errors, run `claude` and `/login`, or use `claude setup-token` and put `CLAUDE_CODE_OAUTH_TOKEN=…` in an `EnvironmentFile=` for `visualtkd-fix.service`.
