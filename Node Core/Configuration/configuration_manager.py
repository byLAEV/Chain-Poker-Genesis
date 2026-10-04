#!/usr/bin/env python3
"""Canonical Node Core configuration manager.

The JSON schema is the structural authority; this module is the single
runtime implementation of the configuration contract and must not redefine
a second schema.
"""
from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path

REQUIRED=("node_core_version","decentralized_storage","protocol_associations","cpg_protocol","network")
CPG_STATES={"NOT_INSTALLED","INSTALLED","ACTIVE"}
STORAGE_STATES={"NOT_PROVISIONED","READY","FAILED","DUAL_STORAGE_READY"}
STORAGE_MODES={"LOCAL","DUAL_STORAGE"}

class ConfigurationError(ValueError):
    pass

def validate_configuration(config: dict, *, fresh_node: bool=True) -> dict:
    if not isinstance(config,dict):
        raise ConfigurationError("configuration must be an object")
    unknown=set(config)-set(REQUIRED)
    missing=set(REQUIRED)-set(config)
    if unknown: raise ConfigurationError("unknown configuration properties: "+", ".join(sorted(unknown)))
    if missing: raise ConfigurationError("missing required configuration properties: "+", ".join(sorted(missing)))
    if not isinstance(config["node_core_version"],str) or not config["node_core_version"]:
        raise ConfigurationError("node_core_version must be a non-empty string")
    storage=config["decentralized_storage"]
    if not isinstance(storage,dict) or set(storage) - {"status","mode"} or "status" not in storage or storage["status"] not in STORAGE_STATES or ("mode" in storage and storage["mode"] not in STORAGE_MODES):
        raise ConfigurationError("invalid decentralized_storage")
    associations=config["protocol_associations"]
    if not isinstance(associations,list) or any(not isinstance(x,str) or not x for x in associations):
        raise ConfigurationError("invalid protocol_associations")
    if len(associations)!=len(set(associations)):
        raise ConfigurationError("duplicate protocol associations")
    cpg=config["cpg_protocol"]
    if cpg not in CPG_STATES:
        raise ConfigurationError("invalid cpg_protocol")
    if fresh_node and cpg!="NOT_INSTALLED":
        raise ConfigurationError("fresh Node Core cannot activate or install CPG")
    network=config["network"]
    if not isinstance(network,dict) or set(network) != {"minimum_protocol_nodes"}:
        raise ConfigurationError("invalid network")
    if network["minimum_protocol_nodes"] != 5:
        raise ConfigurationError("minimum_protocol_nodes must be 5")
    return config

def load(path: Path, *, fresh_node: bool=True) -> dict:
    try:
        data=json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        raise ConfigurationError("configuration could not be loaded") from exc
    return validate_configuration(data,fresh_node=fresh_node)

def canonical_json(config: dict) -> str:
    return json.dumps(validate_configuration(config,fresh_node=False),sort_keys=True,separators=(",",":"))

class ConfigurationManager:
    def __init__(self,path: Path):
        self.path=Path(path)
        self._configuration=None

    def load(self) -> dict:
        self._configuration=load(self.path)
        return dict(self._configuration)

    def get(self) -> dict:
        if self._configuration is None:
            return self.load()
        return dict(self._configuration)

    def validate(self, config: dict) -> dict:
        return validate_configuration(config, fresh_node=False)

    def set_storage_mode(self, mode: str, *, readiness=None) -> dict:
        if mode not in STORAGE_MODES:
            raise ConfigurationError("invalid storage mode")
        if mode == "DUAL_STORAGE":
            if not readiness or readiness.get("dual_storage_ready") is not True:
                raise ConfigurationError("Dual Storage requires verified provider coherence")
            return self.update({"decentralized_storage": {"status": "DUAL_STORAGE_READY", "mode": "DUAL_STORAGE"}})
        current = self.get()["decentralized_storage"]
        status = "READY" if current["status"] != "NOT_PROVISIONED" else "NOT_PROVISIONED"
        return self.update({"decentralized_storage": {"status": status, "mode": "LOCAL"}})

    def update(self, changes: dict) -> dict:
        if not isinstance(changes, dict):
            raise ConfigurationError("configuration changes must be an object")
        current = self.get()
        candidate = dict(current)
        candidate.update(changes)
        # Configuration Manager never installs/activates CPG.
        validated = validate_configuration(candidate, fresh_node=True)
        payload = json.dumps(validated, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".node-config.", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        self._configuration = dict(validated)
        return dict(validated)
