# Node Core Cryptography — Core Crypto External References

These pinned repositories are external implementation references for the Node Core Cryptography layer.

Research targets:
- private-key signing;
- public-key verification and identity linkage;
- secp256k1 / ECDSA / Schnorr;
- authenticated encryption and decryption;
- hashing and key derivation;
- key exchange;
- Lightning authenticated cryptographic channels;
- Bitcoin cryptographic integration.

Target Node Core boundary:

EXTERNAL PRIVATE KEY
    ↓
SIGN / DECRYPT / KEY OPERATION
    ↓
CRYPTOGRAPHIC RESULT
    ↓
NODE CORE VERIFICATION
    ↓
PUBLIC KEY / KEY ID / FINGERPRINT
    ↓
IDENTITY BINDING

Private keys MUST remain outside the Node Core identity registry. A future secure provider may expose signing/decryption operations without exposing raw private key material.

These repositories are REFERENCE_ONLY. They are not automatically CPG code. Before adapting code, verify license, copyright, dependencies, threat model and whether the primitive is actually appropriate for the required operation.
