# Node Core — Implementation Matrix
Status: RECONCILED IMPLEMENTATION BASELINE

**Verification evidence:** GitHub Actions Node Core Verification Run #561 (`794aa43f2561a252efbb851fbf51ff7ea2e94296`) — all workflow gates PASS.

| Subsystem | Defined | Reference implementation | Remaining implementation |
|---|---|---|---|
| Bootstrap | YES | PARTIAL/EXISTING | clean install closure |
| Identity | YES | PARTIAL | persistence, credentials, binding, recovery |
| Configuration | YES | PARTIAL | complete schema/runtime validation |
| Node Manager | YES | PARTIAL | canonical state machine + management events |
| Runtime | YES | PARTIAL | full readiness/degraded/restart behavior |
| Engine Runtime | YES | PARTIAL | isolation, dependency/resource controls |
| Cryptography | YES | PARTIAL | encryption/decryption, signatures, formal profiles |
| Consensus | YES | PARTIAL | formal node-level contract and verification |
| Time | YES | PARTIAL | validation, reference status, logical tick, synchronization contract |
| Storage | YES | IMPLEMENTED/PARTIAL | live Kubo and full failure matrix |
| Network | YES | IMPLEMENTED/PARTIAL | authenticated production transport, discovery, live synchronization |
| Security | YES | PARTIAL | audit, trust, credential, secure configuration |
| Recovery | YES | PARTIAL | journal/reconciliation/full failure recovery |
| API | YES | PARTIAL | full command/service surface |
| CLI | YES | PARTIAL | complete operational command surface |
| Protocol Interface | YES | IMPLEMENTED/PARTIAL | full installation lifecycle |
| Tests | YES | PARTIAL | complete vectors/integration/clean environment |
| Release/Integrity | YES | IMPLEMENTED/PARTIAL | final closure evidence |

## Status semantics
- SPECIFICATION: defined but no accepted executable implementation.
- PARTIAL: executable boundary exists but required scope remains.
- IMPLEMENTED: required scope has executable implementation.
- VERIFIED: implementation plus automated and environmental evidence.
