"""External credential verification boundary; private keys stay outside Node Core."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class CredentialReference:
    credential_type: str
    public_key: str
    key_id: str | None = None
    provenance: str | None = None

@dataclass(frozen=True)
class VerificationResult:
    result: str
    credential_type: str
    subject: str | None
    verifier: str
    reason: str | None = None

class CredentialVerifier(Protocol):
    def verify(self, payload: bytes, signature: bytes, credential: CredentialReference) -> VerificationResult: ...

class Ed25519CredentialVerifier:
    name="ed25519"
    def verify(self,payload:bytes,signature:bytes,credential:CredentialReference)->VerificationResult:
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            key=Ed25519PublicKey.from_public_bytes(bytes.fromhex(credential.public_key))
            key.verify(signature,payload)
            return VerificationResult("VERIFIED",credential.credential_type,credential.key_id,self.name)
        except Exception as exc:
            return VerificationResult("INVALID",credential.credential_type,credential.key_id,self.name,str(exc))
