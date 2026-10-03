"""Canonical Node Core Identity object validation."""
from __future__ import annotations
from dataclasses import asdict
from typing import Any
from .identity_core import NodeIdentity, canonicalize

class IdentitySchemaError(ValueError): pass

def canonical_identity(identity: NodeIdentity) -> bytes:
    return canonicalize(identity.canonical_record())

def validate_identity_record(record: dict[str, Any]) -> NodeIdentity:
    required={"identity_version","node_id","public_key_algorithm","public_key","creation_timestamp","status","registration_reference","verification_reference"}
    missing=required-set(record)
    if missing: raise IdentitySchemaError(f"missing identity fields: {sorted(missing)}")
    identity=NodeIdentity(**record)
    if not identity.validate(): raise IdentitySchemaError("invalid canonical Node Identity")
    return identity
