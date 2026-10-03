"""Protocol-controlled identity request validation."""
from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass(frozen=True)
class IdentityRequest:
    request_id:str
    request_version:str
    request_type:str
    issuer_reference:str
    target_node_life_id:str
    required_property:str
    required_proof_type:str
    sequence_number:int
    issued_at:int
    expires_at:int
    verification_policy:str

class IdentityRequestValidator:
    def validate(self,request:IdentityRequest,expected_target:str,now:int|None=None,previous_sequence:int|None=None)->None:
        current=int(time.time()) if now is None else now
        if request.target_node_life_id!=expected_target: raise ValueError("request target mismatch")
        if request.expires_at<current: raise ValueError("request expired")
        if request.issued_at>current: raise ValueError("request issued in future")
        if previous_sequence is not None and request.sequence_number!=previous_sequence+1: raise ValueError("invalid request sequence")
