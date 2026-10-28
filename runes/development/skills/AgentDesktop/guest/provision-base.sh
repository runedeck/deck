#!/usr/bin/env bash
# Provision the agent base image. Runs as root inside the guest.
# Mirrors cua's Linux desktop stack (X11, AT-SPI, no snaps) and adds the
# agent toolchain. Ends by emptying /etc/machine-id for linked clones.
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
# prlctl exec starts commands with HOME=/ and a PATH without /usr/local;
# npm, pipx and gpg need a real home, and the checks need the installed tools.
export HOME=/root
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

readonly mozilla_fingerprint=35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3
readonly mozilla_key=/etc/apt/keyrings/packages.mozilla.org.asc
# apt verifies as the _apt user, and prlctl exec runs with umask 077, so every
# file apt reads must be made world-readable. This also repairs a rerun.
umask 022
[ ! -f "$mozilla_key" ] || chmod 0644 "$mozilla_key"

echo "== archive packages"
apt-get update -qq
apt-get install -y -qq --no-install-recommends \
    at-spi2-core libatk-adaptor libgail-common python3-gi python3-pyatspi \
    gir1.2-atspi-2.0 gir1.2-gtk-3.0 gsettings-desktop-schemas \
    wmctrl xclip x11-xserver-utils x11-apps xauth imagemagick \
    fonts-dejavu-core fonts-liberation \
    ca-certificates gnupg wget unzip zip tmux fd-find ffmpeg \
    bubblewrap socat gh nodejs npm pipx

echo "== firefox from the Mozilla APT repository"
install -d -m 0755 /etc/apt/keyrings
wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O "$mozilla_key"
chmod 0644 "$mozilla_key"
if ! gpg --homedir "$(mktemp -d)" -n -q --import --import-options import-show "$mozilla_key" | grep -q "$mozilla_fingerprint"; then
    echo "Mozilla signing key fingerprint does not match $mozilla_fingerprint" >&2
    exit 1
fi
cat > /etc/apt/sources.list.d/mozilla.sources <<'EOF'
Types: deb
URIs: https://packages.mozilla.org/apt
Suites: mozilla
Components: main
Signed-By: /etc/apt/keyrings/packages.mozilla.org.asc
EOF
chmod 0644 /etc/apt/sources.list.d/mozilla.sources
cat > /etc/apt/preferences.d/mozilla <<'EOF'
Package: firefox*
Pin: release o=Ubuntu
Pin-Priority: -1
EOF
apt-get update -qq
apt-get install -y -qq firefox
# Privacy defaults, plus the Terms of Use, which the owner accepted on
# 2026-10-26 for every agent that uses this browser (SkipTermsOfUse).
install -d -m 0755 /etc/firefox/policies
cat > /etc/firefox/policies/policies.json <<'EOF'
{
    "policies": {
        "DisableTelemetry": true,
        "DisableFirefoxStudies": true,
        "DontCheckDefaultBrowser": true,
        "SkipTermsOfUse": true
    }
}
EOF

echo "== agent CLIs from npm"
npm install -g --no-fund --no-audit @anthropic-ai/claude-code @openai/codex

echo "== uv through pipx, installed for every user"
[ -x /usr/local/bin/uv ] || PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install uv

echo "== jj from its GitHub release"
jj_tag=$(curl -fsSL https://api.github.com/repos/jj-vcs/jj/releases/latest | python3 -c 'import json, sys; print(json.load(sys.stdin)["tag_name"])')
curl -fsSL "https://github.com/jj-vcs/jj/releases/download/${jj_tag}/jj-${jj_tag}-aarch64-unknown-linux-musl.tar.gz" | tar -xz -C /usr/local/bin ./jj
chmod 0755 /usr/local/bin/jj

echo "== accessibility on in the agent session"
cat > /usr/local/bin/agent-a11y-on <<'EOF'
#!/bin/sh
# Announce an assistive technology so GTK, Qt, Chromium and Electron apps
# build their AT-SPI trees, as cua-driver does when it starts.
gsettings set org.gnome.desktop.interface toolkit-accessibility true 2>/dev/null
busctl --user set-property org.a11y.Bus /org/a11y/bus org.a11y.Status IsEnabled b true 2>/dev/null
exit 0
EOF
chmod 0755 /usr/local/bin/agent-a11y-on
cat > /etc/xdg/autostart/agent-a11y.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Agent accessibility
Exec=/usr/local/bin/agent-a11y-on
EOF

echo "== keep the agent desktop unlocked and awake"
# The agent has no password, so a locked screen ends computer use for good.
install -d -o agent -g agent /home/agent/.config/autostart
printf '[Desktop Entry]\nType=Application\nName=Screen Locker\nHidden=true\n' > /home/agent/.config/autostart/light-locker.desktop
chown agent:agent /home/agent/.config/autostart/light-locker.desktop
cat > /etc/xdg/autostart/agent-no-blank.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Agent display stays on
Exec=xset s off -dpms
EOF

echo "== versions"
firefox --version
node --version
npm --version
claude --version
codex --version
gh --version | head -1
jj --version
uv --version
fdfind --version
python3 -c 'import pyatspi; print("pyatspi ok")'

echo "== reset for linked clones"
apt-get clean
truncate -s 0 /etc/machine-id
echo "provision done"
