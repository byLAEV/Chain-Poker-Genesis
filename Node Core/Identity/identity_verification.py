"""Durable verification-result model."""
from __future__ import annotations
from dataclasses import dataclass,asdict
import hashlib
from .identity_core import canonicalize

RESULTS={"VERIFIED","UNVERIFIED","INVALID","EXPIRED","REJECTED"}

@dataclass(frozen=True)
class VerificationRecord:
    verification_id:str
    request_id:str|None
    subject_reference:str
    verification_type:str
    result:str
    verified_claim_reference:str|None
    proof_reference:str|None
    verified_at:int
    verifier_reference:str
    verification_policy_version:str
    integrity_hash:str

def create_verification_record(verification_id,request_id,subject_reference,verification_type,result,verified_at,verifier_reference,policy_version,claim=None,proof=None):
    if result not in RESULTS: raise ValueError("invalid verification result")
    body={"verification_id":verification_id,"request_id":request_id,"subject_reference":subject_reference,"verification_type":verification_type,"result":result,"verified_claim_reference":claim,"proof_reference":proof,"verified_at":verified_at,"verifier_reference":verifier_reference,"verification_policy_version":policy_version}
    return VerificationRecord(**body,integrity_hash=hashlib.sha256(canonicalize(body)).hexdigest())
