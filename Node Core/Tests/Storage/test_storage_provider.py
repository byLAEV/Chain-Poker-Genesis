#!/usr/bin/env python3
"""Reference tests for the Node Core storage provider boundary."""

from __future__ import annotations

import tempfile
from pathlib import Path

from bootstrap_node import main as bootstrap_main
from storage_provider import LocalStorageProvider

def bootstrap(target):
    import sys
    old = sys.argv
    try:
        sys.argv = ['bootstrap_node.py', str(target)]
        assert bootstrap_main() == 0
    finally:
        sys.argv = old

def main():
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / 'node'
        bootstrap(target)
        provider = LocalStorageProvider(target)
        status = provider.status()
        assert status['provider_type'] == 'LOCAL'
        assert status['status'] == 'READY'
        metadata = provider.put('record', 'provider-record-0001', {'type':'NODE_CORE_PROVIDER_TEST','status':'VALID'})
        assert provider.exists('record', 'provider-record-0001')
        assert provider.verify('record', 'provider-record-0001', metadata['content_hash'])
        description = provider.describe('record', 'provider-record-0001')
        assert description['provider_type'] == 'LOCAL'
        assert description['content_hash'] == metadata['content_hash']
        assert provider.delete('record', 'provider-record-0001') is True
        assert provider.exists('record', 'provider-record-0001') is False

        try:
            provider.put("protocol-reserved", "blocked-provider-write", {"x": 1})
        except Exception:
            pass
        else:
            raise AssertionError("provider bypassed protocol-reserved write boundary")

        print('status = VERIFIED')
        print('provider = LOCAL')
        print('external_provider = NOT_PROVISIONED')

if __name__ == '__main__':
    main()