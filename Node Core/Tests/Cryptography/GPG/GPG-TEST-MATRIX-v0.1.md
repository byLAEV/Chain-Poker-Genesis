# Node Core GPG Test Matrix v0.1

| ID | Test | Expected result |
|---|---|---|
| GPG-KEY-001 | public key discovery | fingerprint resolved |
| GPG-KEY-002 | unknown fingerprint | rejected |
| GPG-SIG-001 | valid detached signature | VERIFIED |
| GPG-SIG-002 | altered payload | INVALID_SIGNATURE |
| GPG-SIG-003 | wrong signer | SIGNER_MISMATCH |
| GPG-SIG-004 | malformed signature | MALFORMED_SIGNATURE |
| GPG-CTX-001 | valid operation binding | VERIFIED |
| GPG-CTX-002 | wrong request identifier | CONTEXT_MISMATCH |
| GPG-CTX-003 | replayed approval | REPLAY_DETECTED |
| GPG-KEY-003 | private key not exposed to Node Core | PASS |
| GPG-HW-001 | GPG agent backed by smartcard | external signing boundary verified |

Production completion requires positive and negative vectors plus runtime validation against an approved GnuPG version.
