#!/bin/sh
set -eu

REPOSITORY="byLAEV/Chain-Poker-Genesis"
INSTALLER_REF="${CPG_INSTALLER_REF:-main}"
RAW_INSTALLER="https://raw.githubusercontent.com/${REPOSITORY}/${INSTALLER_REF}/Installer/install.py"

say() {
    printf '%s\n' "$*"
}

is_termux() {
    [ -n "${TERMUX_VERSION:-}" ] || printf '%s' "${PREFIX:-}" | grep -q 'com.termux'
}

if is_termux; then
    if ! command -v pkg >/dev/null 2>&1; then
        say "ERROR: Termux package manager 'pkg' is required."
        exit 1
    fi
    say "Termux detected. Installing native Python dependencies..."
    pkg install -y python-cryptography
    PYTHON="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    say "ERROR: Python 3 is required to install Node Core on Linux."
    say "Install Python 3, its venv module, and pip using your Linux distribution package manager."
    exit 1
fi

if ! "$PYTHON" - <<'PY'
import sys
if sys.version_info < (3, 9):
    raise SystemExit(1)
PY
then
    say "ERROR: Node Core requires Python 3.9 or newer."
    exit 1
fi

TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t cpg-installer)"
trap 'rm -rf "$TMP_DIR"' EXIT
INSTALLER="$TMP_DIR/install.py"

"$PYTHON" - "$RAW_INSTALLER" "$INSTALLER" <<'PY'
import sys
import urllib.request

url, destination = sys.argv[1], sys.argv[2]
request = urllib.request.Request(
    url,
    headers={"User-Agent": "Chain-Poker-Genesis-Node-Core-Launcher/1.4.0"},
)
with urllib.request.urlopen(request, timeout=60) as response, open(destination, "wb") as output:
    output.write(response.read())
PY

exec "$PYTHON" "$INSTALLER" --ref "$INSTALLER_REF" "$@"
