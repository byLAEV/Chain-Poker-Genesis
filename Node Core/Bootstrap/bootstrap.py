#!/usr/bin/env python3
"""Canonical public Bootstrap API for the fixed Node Core substrate."""
from __future__ import annotations
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
for name in ("Installer", "Initialization", "Verification", "Recovery"):
    sys.path.insert(0, str(BASE / name))

from bootstrap_node import install, BootstrapInstallationError
from node_initializer import initialize
from bootstrap_verifier import verify
from bootstrap_recovery_impl import recover

class Bootstrap:
    version = "1.0.0"
    def initialize(self, target):
        return initialize(Path(target))
    def verify(self, target):
        return verify(Path(target))
    def recover(self, target):
        return recover(Path(target))
    def install(self, target):
        return install(Path(target))
    def bootstrap(self, target):
        return self.install(Path(target))

__all__ = ["Bootstrap", "BootstrapInstallationError"]
