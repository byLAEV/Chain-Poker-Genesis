#!/usr/bin/env python3
"""Public Bootstrap coordinator for Node Core."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent
for name in ("Initialization","Verification","Recovery"):
    sys.path.insert(0,str(BASE/name))
from node_initializer import initialize
from bootstrap_verifier import verify
from bootstrap_recovery_impl import recover

class Bootstrap:
    version="1.0.0"
    def initialize(self,target): return initialize(Path(target))
    def verify(self,target): return verify(Path(target))
    def recover(self,target): return recover(Path(target))
    def bootstrap(self,target):
        initialization=self.initialize(target)
        verification=self.verify(target)
        return {"initialization":initialization,"verification":verification}
