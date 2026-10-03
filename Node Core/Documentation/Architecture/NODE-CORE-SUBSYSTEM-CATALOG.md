# Node Core — Subsystem Catalog
Status: ARCHITECTURAL INVENTORY / IMPLEMENTATION TARGET
Version: 1.0

This catalog completes the Node Core structural target from the information already defined in the repository. A directory or contract listed here does not imply implementation.

## 1. Bootstrap
- Installer
- Initialization
- Verification
- Recovery Bootstrap
- Environment detection
- Dependency verification
- Installation manifest validation
- Clean-install verification

## 2. Identity
- Identity Manager
- Node Identity schema
- Node ID derivation
- Node Life
- Identity validation
- Credential boundary
- Identity binding
- Identity request/verification
- Identity recovery
- Identity persistence

## 3. Configuration
- Configuration Manager
- canonical configuration schema
- defaults
- environment configuration
- validation
- immutable/controlled parameters
- configuration integrity
- configuration migration/versioning

## 4. Node Manager
- lifecycle controller
- readiness coordinator
- engine registry
- protocol registry
- status
- management events
- recovery routing
- protocol-installation requests

## 5. Runtime
- node state
- lifecycle
- readiness
- health
- service startup/shutdown
- dependency ordering
- degraded mode
- graceful shutdown

## 6. Engine Runtime
- engine registry
- engine manifest
- engine version
- dependency declaration
- load
- initialize
- start
- stop
- isolation/resource boundary
- engine state

## 7. Cryptography
- cryptographic primitives
- hashing
- HMAC
- Merkle roots
- encryption/decryption service boundary
- signature generation/verification boundary
- key derivation boundary
- randomness
- cryptographic profiles
- algorithm/version manifest

## 8. Consensus Infrastructure
- canonical serialization
- state hashing
- transition validation
- evidence
- ordering boundary
- node-level consensus interface
- protocol-specific consensus exclusion

## 9. Time
- system time
- external reference time
- network-observed time
- reference epoch
- logical/sequential time
- timestamp validation
- logical tick
- reference status
- synchronization specification boundary

## 10. Storage
- Storage API
- Storage Manager
- Storage Locator
- Object Registry
- Metadata Store
- Local Provider
- Kubo/IPFS Provider
- synchronization state
- operation queue
- integrity verification
- policy engine
- retention
- quarantine
- recovery
- backup
- versioning
- idempotency
- object identity
- content hash/CID separation

## 11. Network
- peer registry
- peer state
- discovery boundary
- transport
- framing
- Node Core handshake
- message envelope
- propagation
- synchronization state
- authenticated transport boundary
- network configuration
- failure/retry policy

## 12. Security
- identity boundary
- credential boundary
- configuration boundary
- storage boundary
- runtime boundary
- engine boundary
- protocol boundary
- network boundary
- recovery boundary
- audit boundary
- fail-closed policy
- integrity
- trust configuration
- revocation/rotation boundary
- sensitive-data protection

## 13. Recovery
- recovery manager
- recovery state
- journal
- checkpoints
- reconciliation
- restore
- quarantine
- retention
- failure classification
- interrupted-operation recovery

## 14. API
- health
- readiness
- node status
- identity
- storage
- engines
- protocols
- verification
- machine-readable errors
- authorization boundary

## 15. CLI
- node status
- readiness
- start
- stop
- recover
- identity
- storage
- engines
- protocols
- verify
- machine-readable output
- deterministic exit codes

## 16. Protocol Interface
- protocol manifest
- compatibility validation
- protocol installation request
- protocol loading
- service capability exposure
- protocol state separation
- activation boundary
- uninstall/deactivation boundary
- CPG exclusion

## 17. Tests / Verification
- unit tests
- integration tests
- failure tests
- recovery tests
- test vectors
- manifest validation
- security tests
- clean-environment tests
- CI
- final readiness evidence

## 18. Release / Integrity / Tools
- release manifest
- integrity verification
- repository audit
- implementation-gap inventory
- canonicalization checks
- installation verification
- completion gate

## Architectural rule
All unfinished entries are targets for implementation. They are not to be represented as implemented merely because the structure exists.
