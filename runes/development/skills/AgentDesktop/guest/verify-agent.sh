#!/usr/bin/env bash
# Verify the agent toolchain and the accessibility tree as the agent user.
# Runs as root inside a fresh clone; switches to agent for every check.
set -uo pipefail
readonly agent_env=(env HOME=/home/agent DISPLAY=:0 XAUTHORITY=/home/agent/.Xauthority DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus PATH=/usr/local/bin:/usr/bin:/bin)

cat > /tmp/verify-as-agent.sh <<'EOF'
set -u
echo "== tools on the agent PATH"
for tool in claude codex jj uv gh node firefox xdotool; do
    printf '%-8s %s\n' "$tool" "$(command -v "$tool" || echo MISSING)"
done
echo "== accessibility flag"
busctl --user get-property org.a11y.Bus /org/a11y/bus org.a11y.Status IsEnabled
echo "== firefox in the AT-SPI tree"
firefox --new-instance about:blank >/dev/null 2>&1 &
sleep 12
python3 - <<'PY'
import pyatspi

desktop = pyatspi.Registry.getDesktop(0)
apps = [desktop.getChildAtIndex(i) for i in range(desktop.childCount)]
names = sorted({app.name for app in apps if app is not None and app.name})
print("applications:", ", ".join(names))

def count(node, depth=0):
    if node is None or depth > 25:
        return 0
    return 1 + sum(count(node.getChildAtIndex(i), depth + 1) for i in range(node.childCount))

for app in apps:
    if app is not None and app.name and "firefox" in app.name.lower():
        print("firefox accessible nodes:", count(app))
PY
xdotool search --name 'Mozilla Firefox' | head -1 | sed 's/^/firefox window id: /'
EOF
chmod 0644 /tmp/verify-as-agent.sh
runuser -u agent -- "${agent_env[@]}" bash /tmp/verify-as-agent.sh
