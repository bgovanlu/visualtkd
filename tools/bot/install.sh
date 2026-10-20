#!/bin/sh
# Install (or refresh) the dev-box bot's systemd user timers. Needs `loginctl enable-linger $USER`
# so they run without a login session, plus bubblewrap and socat for Claude Code's sandbox.
set -e
cd "$(dirname "$0")"
for b in bwrap socat; do command -v $b >/dev/null || { echo "missing $b (apt install bubblewrap socat)"; exit 1; }; done
mkdir -p ~/.config/systemd/user
for u in systemd/*.service systemd/*.timer; do ln -sf "$PWD/$u" ~/.config/systemd/user/; done
systemctl --user daemon-reload
systemctl --user enable --now visualtkd-fix.timer visualtkd-ship.timer
systemctl --user list-timers 'visualtkd-*'
