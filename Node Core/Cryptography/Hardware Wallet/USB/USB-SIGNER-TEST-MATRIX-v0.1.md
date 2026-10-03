# USB Hardware Signer Test Matrix v0.1

| ID | Test | Expected result | Status |
|---|---|---|---|
| USB-001 | no device connected | deterministic `DEVICE_NOT_FOUND` | pending |
| USB-002 | enumerate connected device | device metadata returned | pending |
| USB-003 | unsupported device | `UNSUPPORTED_DEVICE` | pending |
| USB-004 | public-key request | public key returned, no private key | pending |
| USB-005 | approval request | device confirmation required | pending |
| USB-006 | user rejects approval | `USER_REJECTED` | pending |
| USB-007 | valid hardware signature | signature verified | pending |
| USB-008 | altered payload after approval | verification fails | pending |
| USB-009 | wrong request identifier | verification fails | pending |
| USB-010 | replayed signature | replay rejected | pending |
| USB-011 | device disconnect during signing | deterministic transport error | pending |
| USB-012 | private-key export request | operation prohibited | pending |
| USB-013 | invalid derivation path | deterministic validation error | pending |
| USB-014 | signer/provider timeout | deterministic timeout | pending |

## Security acceptance

No test may require exporting a seed, master private key, child private key, PIN, or passphrase into Node Core.
