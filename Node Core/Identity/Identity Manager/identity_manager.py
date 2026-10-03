#!/usr/bin/env python3
"""Stable import boundary for the Node Core Identity manager."""
from pathlib import Path
import importlib.util
import sys

_IMPL = Path(__file__).resolve().parents[1] / "identity_core.py"
_SPEC = importlib.util.spec_from_file_location("node_core_identity_core", _IMPL)
_MODULE = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

IdentityManager = _MODULE.IdentityManager
NodeIdentity = _MODULE.NodeIdentity
NodeLife = _MODULE.NodeLife

__all__ = ["IdentityManager", "NodeIdentity", "NodeLife"]
