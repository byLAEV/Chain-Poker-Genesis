# Node Core — Service Catalog
Status: ARCHITECTURAL BASELINE

| Service | Consumed by | Must remain protocol-neutral |
|---|---|---|
| Identity | Node Manager, Security, Network | YES |
| Cryptography | Identity, Storage, Security, Engines | YES |
| Time | Runtime, Network, Storage, Engines | YES |
| Storage | Runtime, Recovery, Protocol Interface | YES |
| Network | Runtime, Protocol Interface, synchronization | YES |
| Security | all Node Core services | YES |
| Recovery | Bootstrap, Runtime, Storage | YES |
| Engine Runtime | Node Manager, Protocol Interface | YES |
| Consensus Infrastructure | Node-level services / protocols through interface | YES |
| API | operators/tools | YES |
| CLI | operators/automation | YES |
| Protocol Interface | external protocols | YES |

No service in this catalog may silently import CPG-specific table, poker, wallet, settlement, rake or ledger semantics.
