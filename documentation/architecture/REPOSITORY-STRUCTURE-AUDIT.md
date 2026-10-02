# Repository Structure Audit

## Project
Chain Poker Genesis by LAEV

## Purpose
This audit defines the structural reorganization required to move the repository from an historically accumulated documentation tree toward an implementation-oriented architecture.

This document is an architectural migration plan. It does not itself move or delete existing files.

## Current Structural Finding
The repository currently mixes:
- protocol and engine specifications;
- rendered PDF specifications;
- implementation-oriented material;
- historical source material;
- Node-related infrastructure;
- protocol-level engines;
- documentation infrastructure;
- installation material;
- standards and governance material.

Several engine directories contain Markdown specifications while their corresponding PDF artifacts remain at repository root. This creates a separation between an engine's human-readable source specification and its rendered document.

The current numbered engine directories also reflect development chronology more than implementation-layer boundaries.

## Canonical Target Layers
The target repository should distinguish the following layers:
1. node-core/ — infrastructure required for a protocol node to exist and operate.
2. protocol-engines/ — protocol-specific functional engines running on the Node Core.
3. implementation/ — reference implementation, schemas, manifests and deterministic test vectors.
4. documentation/ — canonical human-readable protocol and architecture documentation.
5. historical/ — historical source material and superseded design artifacts retained for provenance.
6. tests/ — executable conformance and integration tests.
7. tools/ — development, generation and validation utilities.
8. .github/ — repository automation and CI.

## Proposed Node Core Boundary
The Node Core should eventually contain, at minimum:
- identity;
- cryptographic identity and primitives;
- key management and lifecycle;
- persistent storage;
- state management;
- event/log model;
- networking;
- synchronization;
- permissions;
- recovery/failure handling;
- versioning.

A protocol engine should not be classified as Node Core merely because it runs on a node.

## Proposed Protocol Engine Layer
Existing numbered engine directories should be evaluated for migration into protocol-engines/, including the currently identified:
- Private Off-Chain Ledger;
- Rake and Settlement;
- Commitment-Reveal Card Dealing;
- Dual Shuffle Card Distribution;
- Table Join;
- Table Wallet;
- Player Node Disconnection Management;
- Monetary Settlement;
- Request and Permission;
- P2P Conflict Resolution;
- Poker Rules;
- and later protocol engines discovered during the complete tree audit.

The historical numeric identifiers should be preserved in migration metadata or documentation where useful, but should not determine the final software package hierarchy.

## Documentation Rule
PDF files are documentation artifacts and should not define implementation boundaries.

Where a PDF corresponds to an engine or specification, the target location should be under the relevant documentation area or an explicitly defined documentation subdirectory of that component.

The canonical source should be the structured specification/manifests used for implementation and verification; PDFs should be treated as rendered/publication artifacts.

## Migration Rules
No file should be deleted solely because it appears duplicated until:
1. its content is compared with the corresponding Markdown/specification;
2. its provenance is recorded;
3. references to it are identified;
4. the canonical replacement is established.

No implementation directory should be created merely to mirror a PDF title.

No Node Core component should be created merely because an existing document mentions the word Node.

## Migration Sequence
1. Freeze the current tree as the migration baseline.
2. Inventory every root-level file and directory.
3. Classify each item by architectural layer.
4. Identify document/specification/PDF relationships.
5. Identify historical/provenance artifacts.
6. Define the final Node Core boundary.
7. Define the final protocol-engine boundary.
8. Produce a file-by-file migration matrix.
9. Create target directories.
10. Move/rename files in a controlled migration commit.
11. Repair internal links and references.
12. Run repository validation and CI.
13. Re-audit the resulting tree.
14. Resume Node Core canonicalization on the normalized tree.

## Immediate Next Deliverable
The next required artifact is a complete file-by-file migration matrix with:

| Current Path | Type | Architectural Layer | Canonical Role | Target Path | Action | Dependency/Reference Impact |
|---|---|---|---|---|---|---|
| pending full inventory | | | | | | |

This matrix must be completed before bulk file movement.

## Non-Destructive Principle
Until the migration matrix is approved, the existing repository remains the source tree. The audit does not authorize deletion or irreversible restructuring.

## Architectural Objective
The final tree must make the following relationship explicit:

LAEV Design Intent
→ Canonical Specification
→ Schemas / Manifests
→ Reference Implementation
→ Tests / Test Vectors
→ Interoperable Implementations

The directory structure must support that progression rather than obscure it.