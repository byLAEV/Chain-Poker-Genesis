"""RISC Zero provider boundary for Node Core zero-knowledge verification.

The adapter deliberately uses a subprocess boundary so the Node Core Python
process does not embed a Rust proving runtime. The exact guest method is
provided by the caller/tooling integration.
"""
from __future__ import annotations
import json
import subprocess

class RiscZeroProvider:
    name="risc0"
    version="0.20.1"
    def __init__(self, verifier_command):
        if not verifier_command:
            raise ValueError("verifier_command is required")
        self.verifier_command=list(verifier_command)
    def capabilities(self): return ("proof_verification", "receipt_verification")
    def verify(self, proof, public_inputs):
        request=json.dumps({"proof":proof,"public_inputs":public_inputs},separators=(",",":")).encode()
        result=subprocess.run(self.verifier_command,input=request,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        if result.returncode != 0:
            return False
        try: return bool(json.loads(result.stdout.decode())["verified"])
        except (ValueError,KeyError): return False
