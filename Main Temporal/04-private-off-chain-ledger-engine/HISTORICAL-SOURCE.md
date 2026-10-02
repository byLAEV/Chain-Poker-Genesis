# Historical Record — 04 Private Off-Chain Ledger Engine

**Source document:** `04. Private Off-Chain Ledger Engine_- Chain Poker Genesis by LAEV.pdf`  
**Protocol:** Chain Poker Genesis by LAEV  
**Historical version:** 1.0  
**Author:** Lerry Alexander Elizondo Villalobos (LAEV)

## Repository treatment

This file records the repository-level treatment of the supplied PDF transcription.

The historical document contains multiple accumulated editions of the same functional specification in English and Spanish. Its common architecture establishes the Private Off-Chain Ledger Engine as the protocol's private historical evidence layer.

### Preserved historical concepts

- Complete protocol event recording
- Chronological private storage
- JSON event structures
- High-precision / UTC timestamps
- Per-event cryptographic hashes
- Optional sequential `previous_hash` relationship
- Merkle Tree consolidation
- Merkle Root generation
- Periodic Bitcoin anchoring
- Private operational data
- Cryptographic verification
- Audit and historical reconstruction
- Integration with protocol engines and Player Nodes

### Historical event scope

The source identifies events such as:

- Node startup and shutdown
- Player Node activation and authentication
- Cryptographic validation
- Network connection and disconnection
- Node synchronization
- Inter-node communication
- Game and poker-hand lifecycle
- Player actions and betting operations
- Internal engine operations
- Configuration and administration
- Security and audit events
- Digital-asset-related operations
- Protocol state transitions

### Important consolidation note

The PDF is treated as a **historical source**, while the engine README is the repository-facing consolidated specification.

The repository should preserve the original PDF itself when its binary file is available. This update was produced from the supplied transcription; no binary PDF was available to the GitHub connector during this update.

## Source integrity note

The historical source uses broad formulations such as “record everything” and describes Bitcoin anchoring as evidence of existence and integrity. The implementation-facing documentation narrows these statements to verifiable software behavior: the ledger preserves recorded events, while the Bitcoin anchor commits to the resulting cryptographic batch representation.

**Status:** Historical source incorporated into repository architecture.
