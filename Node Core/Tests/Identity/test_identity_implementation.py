#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]/"Identity"
sys.path.insert(0,str(BASE))
from identity_core import IdentityManager, reconstruct_lifecycle
from credential_interface import Ed25519CredentialVerifier, CredentialReference
def main():
    manager=IdentityManager()
    identity, private=manager.create_identity(timestamp=1000)
    assert identity.validate() and len(private)==32
    manager.initialize(timestamp=1001); manager.activate(timestamp=1002)
    snap=manager.snapshot()
    assert reconstruct_lifecycle(snap["node_life"]["state_history"])=="ACTIVE"
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        key=Ed25519PrivateKey.from_private_bytes(private)
        payload=b"node-core-identity-test"
        result=Ed25519CredentialVerifier().verify(payload,key.sign(payload),CredentialReference("Ed25519",identity.public_key,"node-key"))
        assert result.result=="VERIFIED"
    except ImportError: pass
    print("Node Core Identity implementation tests: PASS")
if __name__=="__main__": main()
