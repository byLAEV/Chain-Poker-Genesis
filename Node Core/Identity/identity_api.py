#!/usr/bin/env python3
"""Public protocol-neutral Identity API."""
from __future__ import annotations
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

from identity_core import IdentityManager


class IdentityAPI:
    def __init__(self):
        self.manager = IdentityManager()

    def create(self, timestamp=None):
        return self.manager.create_identity(timestamp)

    def validate(self, verification_reference=None):
        return self.manager.validate_identity(verification_reference)

    def register(self, registration_reference):
        return self.manager.register(registration_reference)

    def initialize(self, timestamp=None, registration_reference="LOCAL_NODE_REGISTRATION"):
        return self.manager.initialize(timestamp, registration_reference)

    def activate(self, timestamp=None, node_core_ready=False):
        return self.manager.activate(timestamp, node_core_ready)

    def snapshot(self):
        return self.manager.snapshot()
