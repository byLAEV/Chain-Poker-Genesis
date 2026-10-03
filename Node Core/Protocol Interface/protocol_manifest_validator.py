"""Validation for external protocol manifests."""
from __future__ import annotations
REQUIRED=("protocol_id","version","engine_id","manifest_hash")
def validate_manifest(manifest):
    if not isinstance(manifest,dict): raise ValueError("manifest must be an object")
    missing=[key for key in REQUIRED if not manifest.get(key)]
    if missing: raise ValueError("missing required fields: "+", ".join(missing))
    capabilities=manifest.get("capabilities",[])
    if not isinstance(capabilities,list) or any(not isinstance(x,str) for x in capabilities):
        raise ValueError("capabilities must be a list of strings")
    return True
