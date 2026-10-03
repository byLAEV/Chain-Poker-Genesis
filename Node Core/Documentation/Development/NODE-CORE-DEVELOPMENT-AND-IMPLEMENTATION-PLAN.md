# Node Core Development and Implementation Plan

**Scope:** Chain Poker Genesis — Node Core only  
**Purpose:** develop Node Core in GitHub until it is reproducibly installable, initializable, verifiable, and operational on a clean local machine.

## 1. Controlled sequence

1. Audit current Node Core structure and references.
2. Normalize and canonicalize names, paths, manifests, and interfaces.
3. Establish implementation contracts for each Node Core subsystem.
4. Implement Bootstrap and Installation.
5. Implement Identity.
6. Implement the Node Core Cryptography layer.
7. Implement Storage and storage-provider behavior.
8. Implement Runtime and Readiness.
9. Implement Network and Synchronization.
10. Implement Recovery.
11. Implement the Protocol Interface boundary.
12. Complete Configuration and Node Core Manifest validation.
13. Complete operational CLI/entry points.
14. Build unit, integration, failure, verification, and test-vector coverage.
15. Integrate all applicable checks into GitHub Actions.
16. Validate the Codespaces development environment.
17. Execute a clean-environment installation and operational verification.
18. Produce the Local Readiness record and close Node Core.

## 2. Phase gate

Every phase follows:

**Specification → Implementation → Test → Verification → Evidence → Gate**

A failed gate returns the phase to implementation. Passing a test does not override an architectural or contract failure.

## 3. Required implementation areas

- Bootstrap / Installer / Initialization / Verification / Recovery
- Identity and cryptographic connection
- Cryptography core
- Storage Manager / Locator / Providers / Object Registry
- Runtime / State / Readiness
- Network / Synchronization
- Recovery
- Protocol Interface / Protocol Installation
- Configuration / Schemas / Manifest
- Release / Integrity
- Tools / Validation
- Tests / Test Vectors
- Operational documentation

## 4. Boundaries

Node Core must not absorb CPG-specific table, poker, settlement, ledger, viewer, or protocol-engine functionality.

Node Core provides the infrastructure and protocol-installation boundary over which a future protocol can operate.

## 5. Completion condition

Node Core is not closed until a clean environment can install, initialize, verify, start, report readiness, restart, and recover the node using repository-defined procedures, with the verification evidence recorded in GitHub.
