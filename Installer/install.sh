#!/bin/sh
set -eu

REPOSITORY="byLAEV/Chain-Poker-Genesis"
INSTALLER_REF="${CPG_INSTALLER_REF:-main}"
RAW_INSTALLER="https://raw.githubusercontent.com/${REPOSITORY}/${INSTALLER_REF}/Installer/install.py"

say() {
    printf '%s\n' "$*"
}

if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    if command -v pkg >/dev/null 2>&1; then
        say "Python is not installed. Installing Python through Termux pkg..."
        pkg install -y python python-cryptography
        PYTHON="python"
    else
        say "ERROR: Python 3 is required to install Node Core."
        exit 1
    fi
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
    headers={"User-Agent": "Chain-Poker-Genesis-Node-Core-Launcher/1.0"},
)
with urllib.request.urlopen(request, timeout=60) as response, open(destination, "wb") as output:
    output.write(response.read())
PY

exec "$PYTHON" "$INSTALLER" --ref "$INSTALLER_REF" "$@"
