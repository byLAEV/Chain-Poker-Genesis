import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"Identity"))
from identity_core import IdentityManager
from identity_schema import validate_identity_record
from credential_interface import CredentialReference,Ed25519CredentialVerifier
from identity_binding import IdentityBinding,calculate_manifest_hash,verify_binding
from identity_requests import IdentityRequest,IdentityRequestValidator
from identity_verification import create_verification_record
from identity_recovery import recover_same_life

class IdentityCompletionTests(unittest.TestCase):
    def test_schema_and_external_signature(self):
        manager=IdentityManager(); identity,private=manager.create_identity(1)
        validate_identity_record(identity.canonical_record())
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        key=Ed25519PrivateKey.from_private_bytes(private); payload=b"identity-test"; sig=key.sign(payload)
        result=Ed25519CredentialVerifier().verify(payload,sig,CredentialReference("ed25519",identity.public_key,"node"))
        self.assertEqual(result.result,"VERIFIED")

    def test_binding(self):
        manager=IdentityManager(); identity,_=manager.create_identity(1)
        b=IdentityBinding("b1",manager.node_life.node_life_id,identity.node_id,"node","ed25519",1,"signature","VERIFIED","")
        b=IdentityBinding(**{**b.__dict__,"manifest_hash":calculate_manifest_hash(b)})
        self.assertTrue(verify_binding(b))

    def test_request_and_verification(self):
        manager=IdentityManager(); identity,_=manager.create_identity(1)
        req=IdentityRequest("r1","1.0","PROPERTY","issuer",manager.node_life.node_life_id,"public-key","signature",0,1,10,"policy-1")
        IdentityRequestValidator().validate(req,manager.node_life.node_life_id,now=5)
        rec=create_verification_record("v1","r1",identity.node_id,"signature","VERIFIED",5,"verifier","1")
        self.assertEqual(rec.result,"VERIFIED")

    def test_recovery_requires_continuity(self):
        manager=IdentityManager(); manager.create_identity(1); manager.initialize(2); manager.activate(3)
        manager.node_life.transition("NODE_TERMINATED","TERMINATED",4)
        event=recover_same_life(manager.node_life,True)
        self.assertEqual(event.state,"RECOVERED")

if __name__=="__main__": unittest.main()
