#!/usr/bin/env python3
"""Canonical Node Core configuration manager.

The JSON schema is the structural authority; this module is the single
runtime implementation of the configuration contract and must not redefine
a second schema.
"""
from __future__ import annotations
import json
from pathlib import Path

REQUIRED=("node_core_version","decentralized_storage","protocol_associations","cpg_protocol")
CPG_STATES={"NOT_INSTALLED","INSTALLED","ACTIVE"}
STORAGE_STATES={"NOT_PROVISIONED","READY","FAILED"}

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
    if not isinstance(storage,dict) or set(storage)!={"status"} or storage["status"] not in STORAGE_STATES:
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
        return validate_configuration(config,fresh_node=False)
