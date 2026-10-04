#!/bin/sh
set -eu

REPOSITORY="byLAEV/Chain-Poker-Genesis"
INSTALLER_REF="${CPG_INSTALLER_REF:-main}"
RAW_INSTALLER="https://raw.githubusercontent.com/byLAEV/Chain-Poker-Genesis/${INSTALLER_REF}/Installer/install.py"

say() {
    printf '%s\n' "$*"
}

if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    if command -v pkg >/dev/null 2>&1; then
        say "Python no está instalado. Instalando Python mediante Termux pkg..."
        pkg install -y python
        if command -v python >/dev/null 2>&1; then
            PYTHON="python"
        else
            say "ERROR: no se pudo instalar Python."
            exit 1
        fi
    else
        say "ERROR: Python 3 es necesario para instalar Node Core."
        say "Instala Python 3 y vuelve a ejecutar este instalador."
        exit 1
    fi
fi

TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t cpg-installer)"
trap 'rm -rf "$TMP_DIR"' EXIT

INSTALLER="$TMP_DIR/install.py"

if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$RAW_INSTALLER" -o "$INSTALLER"
elif command -v wget >/dev/null 2>&1; then
    wget -qO "$INSTALLER" "$RAW_INSTALLER"
else
    say "ERROR: se necesita curl o wget para descargar el instalador."
    exit 1
fi

exec "$PYTHON" "$INSTALLER" --ref "$INSTALLER_REF" "$@"
