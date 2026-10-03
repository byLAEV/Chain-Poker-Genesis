"""Immutable binding between Node Life and an external cryptographic identity."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass,asdict
from .identity_core import canonicalize

@dataclass(frozen=True)
class IdentityBinding:
    binding_id:str
    node_life_id:str
    node_id:str
    credential_key_id:str
    credential_type:str
    created_at:int
    binding_signature:str
    verification_state:str
    manifest_hash:str

def binding_payload(binding:IdentityBinding)->bytes:
    d=asdict(binding); d.pop("binding_signature",None); d.pop("manifest_hash",None)
    return canonicalize(d)

def calculate_manifest_hash(binding:IdentityBinding)->str:
    return hashlib.sha256(binding_payload(binding)).hexdigest()

def verify_binding(binding:IdentityBinding)->bool:
    return binding.verification_state=="VERIFIED" and binding.manifest_hash==calculate_manifest_hash(binding)
