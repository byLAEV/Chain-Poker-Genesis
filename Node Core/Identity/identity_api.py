#!/usr/bin/env python3
"""Public protocol-neutral Identity API."""
from __future__ import annotations
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/"Identity Manager"))
from identity_manager import IdentityManager
class IdentityAPI:
    def __init__(self): self.manager=IdentityManager()
    def create(self,timestamp=None): return self.manager.create_identity(timestamp)
    def initialize(self,timestamp=None): return self.manager.initialize(timestamp)
    def activate(self,timestamp=None): return self.manager.activate(timestamp)
    def snapshot(self): return self.manager.snapshot()
