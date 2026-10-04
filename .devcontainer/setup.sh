#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/Chain-Poker-Genesis

echo "[1/6] Initializing all repository submodules..."
git submodule sync --recursive
git submodule update --init --recursive

echo "[2/6] Installing Node Core Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r "Node Core/Cryptography/requirements.txt"

echo "[3/6] Installing Node Core OpenPGP dependencies..."
if [ -f "Node Core/Cryptography/OpenPGP/package.json" ]; then
  cd "Node Core/Cryptography/OpenPGP"
  npm install
  cd /workspaces/Chain-Poker-Genesis
fi

echo "[4/6] Running Node Core structural audit..."
python scripts/node_core_audit.py

echo "[5/6] Compiling Node Core and Main Temporal Python sources..."
python - <<'PY'
import compileall
import sys
ok = True
for root in ("Node Core", "Main Temporal"):
    ok = compileall.compile_dir(root, quiet=1) and ok
if not ok:
    raise SystemExit(1)
print("[PASS] Python compilation: Node Core + Main Temporal")
PY

echo "[6/6] Codespace installation complete."
echo "Repository: Chain Poker Genesis byLAEV"
echo "Node Core: installed and audited"
echo "CPG protocol: not installed by Node Core bootstrap"
