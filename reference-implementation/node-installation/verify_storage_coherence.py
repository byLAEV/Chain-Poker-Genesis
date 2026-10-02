#!/usr/bin/env python3
"""Verify Node Core local storage coherence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_PATHS = [
    'node-storage',
    'node-storage/identity',
    'node-storage/cryptography',
    'node-storage/configuration',
    'node-storage/state',
    'node-storage/records',
    'node-storage/recovery',
    'node-storage/protocol',
]

def fail(reason):
    print('status = FAILED')
    print(f'coherence = {reason}')
    return 1

def main():
    if len(sys.argv) != 2:
        return fail('INVALID_ARGUMENTS')
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        return fail('MISSING_OBJECT')
    for path in REQUIRED_PATHS:
        if not (root / path).is_dir():
            return fail('STRUCTURE_MISMATCH')
    manifest_path = root / 'node-storage/state/storage-manifest.json'
    if not manifest_path.is_file():
        return fail('MISSING_OBJECT')
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return fail('MISSING_OBJECT')
    if manifest.get('root') != 'node-storage':
        return fail('STRUCTURE_MISMATCH')
    if manifest.get('required_paths') != REQUIRED_PATHS:
        return fail('STRUCTURE_MISMATCH')
    for relative in [
        'node-storage/identity/node-identity.json',
        'node-storage/configuration/node-config.json',
        'node-storage/recovery/recovery.json',
    ]:
        if not (root / relative).is_file():
            return fail('MISSING_OBJECT')
    print('status = VERIFIED')
    print('coherence = COHERENT')
    print('network_synchronization = NOT_EVALUATED')
    print('external_provider = NOT_PROVISIONED')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())