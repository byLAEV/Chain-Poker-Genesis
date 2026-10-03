"""Minimal public identity reference package."""
from __future__ import annotations
from .identity_core import NodeIdentity,NodeLife

def public_reference(identity:NodeIdentity,life:NodeLife)->dict:
    return {"node_id":identity.node_id,"identity_version":identity.identity_version,"public_key_algorithm":identity.public_key_algorithm,"public_key":identity.public_key,"node_life_id":life.node_life_id,"lifecycle_state":life.state}
