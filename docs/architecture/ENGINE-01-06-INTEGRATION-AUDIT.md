# Engine 01–06 Integration Audit

**Chain Poker Genesis by LAEV**
**Audit scope:** Installation, Graphical Interface, Cryptographic Connection, Private Off-Chain Ledger, Rake/Settlement Flow, Commitment/Reveal Card Dealing.
**Status:** Working integration audit — not yet normative.

## 1. Purpose

This audit checks whether Engines 01–06 can coexist without silently assigning the same responsibility to multiple components or leaving critical responsibilities ownerless.

The audit is based on the structured repository documentation currently available and the historical-source boundaries already established. It deliberately marks unresolved matters instead of inventing protocol rules.

## 2. Responsibility matrix

| Area | 01 | 02 | 03 | 04 | 05 | 06 | Owner |
|---|---|---|---|---|---|---|---|
| Node installation | X | | | | | | 01 |
| General graphical navigation | | X | | | | | 02 |
| Cryptographic connection/session | | | X | | | | 03 |
| Identity/signature services | | | X | | | X consumes | 03 |
| Event persistence | | | | X | X emits | X emits | 04 |
| Merkle consolidation | | | | X | | | 04 |
| Bitcoin anchoring evidence | | | | X | | | 04 |
| Rake calculation | | | | | X | | 05 |
| Final monetary transfer | | | | | request | | Monetary Settlement Engine |
| Card commitment | | | | evidence | | X | 06 |
| Card encryption/private payload | | | | evidence only | | X | 06 |
| Card reveal verification | | | | evidence | | X | 06 |
| Poker legality of reveal | | | | | | consumes | Poker Rules Engine |
| Reveal authorization | | | | evidence | | requests | Requests & Permissions |
| Card randomness/deck generation | | | | evidence | | consumes | Dedicated randomness/dealer mechanism |
| Table wallet state | | | | evidence | consumes | | Table Wallet Engine |

## 3. Integration flow

The intended cross-engine flow is:

Installation
→ Cryptographic Connection
→ Node ready
→ Graphical Interface
→ protocol/table lifecycle
→ cryptographic identity
→ game state
→ card assignment / commitment
→ gameplay
→ hand completion
→ rake calculation
→ settlement authorization
→ monetary settlement
→ ledger evidence / replay

Engine 04 is cross-cutting persistence and verification infrastructure rather than the owner of the business rules above it.

## 4. Finding A — signature versus encryption

**Status: RESOLVED IN ENGINE 06 RECONSTRUCTION.**

The historical Engine 06 wording can be read as if the wallet signature itself provides private-card confidentiality. A digital signature provides authorization/integrity properties but does not encrypt card data.

The reconstructed Engine 06 therefore separates:

- commitment;
- encryption;
- signature;
- reveal.

This distinction must remain consistent in future engines.

## 5. Finding B — randomness ownership

**Status: OPEN / OWNER REQUIRED.**

Engine 06 must not become the implicit owner of deck randomness merely because it performs card commitments.

The repository already identifies multi-party Commit-Reveal, deck-cut randomness and burn-card randomness at the protocol level. A dedicated Dealer/Card Distribution/Randomness specification must define the source and lifecycle of entropy.

Engine 06 consumes the resulting card assignment and commits to it.

## 6. Finding C — wallet identity versus encryption keys

**Status: OPEN.**

Engine 03 provides cryptographic connection/identity functions. Engine 06 uses player authorization and private-card encryption. The repository must not assume that a signing key can automatically decrypt card ciphertext.

A future key-management specification must define whether encryption uses:

- a separate encryption key;
- wallet-derived key material;
- a key-agreement mechanism;
- an application/session key protected by wallet authorization;
- or another formally specified mechanism.

Until then, Engine 06 correctly treats the relationship as an interface dependency rather than an implementation fact.

## 7. Finding D — reveal authority

**Status: CONSISTENT BOUNDARY.**

Engine 06 verifies a reveal. It does not decide that poker rules require the reveal.

The authority chain is:

Poker Rules Engine
→ reveal requirement
→ Requests & Permissions Engine
→ authorization
→ Engine 06 verification
→ public-state transition

The GUI must not be inserted as an authority in this chain.

## 8. Finding E — ledger privacy versus replay

**Status: OPEN / REPLAY CONTRACT REQUIRED.**

Engine 04 is designed as a private event-history layer while the protocol also requires complete hand replay.

Those goals are compatible only if the replay specification defines what private material is retained, who can decrypt it, and how authorized replay reconstructs the same state.

A public or replicated ledger must not require plaintext private cards merely to make replay possible.

Required future distinction:

- public replay evidence;
- authorized private replay material;
- commitment proofs;
- randomness/deck reconstruction material;
- revealed-card data.

## 9. Finding F — Engine 05 versus Monetary Settlement Engine

**Status: CONSISTENT AFTER STRUCTURING.**

Engine 05 calculates and records the economic obligation. The Monetary Settlement Engine executes the final monetary transfer.

This prevents Engine 05 from becoming both calculator and payment executor.

The canonical bridge is the stable Rake Obligation ID.

## 10. Finding G — Engine 05 determinism

**Status: OPEN / PRECISION SPECIFICATION REQUIRED.**

The 3% / 11% / 89% formulas are deterministic mathematically, but Bitcoin settlement requires integer-satoshi rules.

Before production compatibility, the protocol must specify:

- conversion to satoshis;
- rounding direction;
- dust handling;
- minimum settlement amount;
- network-fee treatment.

Until these are fixed, two implementations could legally interpret the same nominal pot differently.

## 11. Finding H — hand completion authority

**Status: OWNER REQUIRED EXPLICITLY.**

Engine 05 must consume an authorized HAND_COMPLETED state transition. It must not infer completion from UI, card reveal, elapsed time or wallet movement.

The Poker Rules/State Machine boundary should therefore expose a canonical hand-completion event.

## 12. Finding I — external settlement entity versus decentralized architecture

**Status: ARCHITECTURAL BOUNDARY TO DOCUMENT.**

The current repository describes Chain Poker Genesis as a decentralized protocol without a central operating company, while Engine 05 documentation describes an external company destination for a configured portion of rake.

These statements are not necessarily technically contradictory: an external destination can exist without controlling protocol execution. However, the architecture must explicitly state that a destination recipient does not acquire protocol authority merely by receiving settlement funds.

This is a governance/economic boundary, not a card-engine boundary.

## 13. Finding J — Installation and runtime trust

**Status: OPEN.**

Engine 01 establishes installation integrity and synchronization. Engine 03 provides cryptographic connection functions. The repository still needs a formal root-of-trust and key-verification specification before an installed node can be considered cryptographically trusted.

The current Engine 01 documentation correctly marks root of trust, signing-key hierarchy, revocation and rollback as unresolved.

## 14. Finding K — GUI authority isolation

**Status: CONSISTENT.**

Engine 02 may display commitment status, reveal status, rake status and verification results, but must not originate authoritative protocol decisions merely because a user clicked a UI control.

Authoritative state transitions must come from the protocol engines and their permission/state contracts.

## 15. Finding L — replay and encrypted cards

**Status: OPEN / CRITICAL FOR FUTURE REPLAY ENGINE.**

If private cards are encrypted and the general ledger stores only commitments and hashes, deterministic replay requires a defined authorized source of the original private inputs or an alternative cryptographic replay proof.

This is especially important if the protocol claims that every completed hand can be reproduced from recorded protocol events.

The future Replay Engine must specify whether replay means:

1. public verification of state transitions;
2. authorized reconstruction of private state;
3. full cryptographic reproduction including hidden inputs.

These are different guarantees.

## 16. Current blockers before declaring 01–06 implementation-ready

1. Define the canonical randomness/deck-generation owner.
2. Define wallet signing-key versus encryption-key architecture.
3. Define the canonical HAND_COMPLETED event.
4. Define integer-satoshi precision for Engine 05.
5. Define settlement-fee treatment.
6. Define private replay material and authorization.
7. Define the formal event schema shared with Engine 04.
8. Define protocol/domain separation for cryptographic hashes and signatures.
9. Define the canonical identity format used consistently by Engines 03–06.
10. Audit the historical Dealer/Card Distribution documents before assigning randomness ownership.

## 17. Current conclusion

Engines 01–06 can be arranged into a coherent modular architecture, but the system should **not yet be treated as implementation-complete**.

The major structural boundary is now clear:

- 01 prepares the node;
- 02 presents the node/protocol interface;
- 03 provides cryptographic connection/identity services;
- 04 preserves verifiable protocol history;
- 05 calculates the rake obligation;
- 06 protects, commits and verifies private cards.

The remaining high-impact gaps are primarily cross-engine contracts rather than additional prose inside an individual engine.

## 18. Next audit target

Before Engine 07 is consolidated, the most important cross-check is the historical card/dealer material, especially documents 16 and 29, followed by the Requests & Permissions document 13 and the Poker Rules document 15.

Those documents determine whether the current Engine 06 boundary correctly separates randomness, dealing, authorization and reveal.

---

**Audit status:** 01–06 structurally aligned with open cross-engine contracts identified.


## 5. Finding B — dual shuffle/distribution boundary

**Status: ARCHITECTURAL CORRECTION APPLIED.**

Card generation/distribution must not be owned ambiguously by Engine 06, Dealer, or the ledger. The repository now defines a supporting dual-shuffle architecture with two compatible implementations:

- **Engine A:** native Chain Poker Genesis shuffle/distribution mechanism;
- **Engine B:** independent verifiable-shuffle / mental-poker adapter.

Only one is authoritative for a given hand. The selected engine is fixed before authoritative card-assignment commitment. The non-selected engine may independently verify the same canonical result where compatibility permits.

The second engine is therefore not a second competing dealer. It reduces implementation monoculture while preserving one canonical hand state.

## 6. Finding C — Engine 06 commitment/reveal boundary

**Status: CORRECTED.**

Engine 06 receives a canonical card-assignment result. It owns private-card commitment, protected-card handling, reveal authorization consumption, and reveal verification. It does not select a shuffle result after seeing private cards.

The selected shuffle engine identifier and version become part of the hand context and are persisted as protocol evidence by Engine 04.

## 7. Finding D — randomness ownership

**Status: OPEN / MUST BE RESOLVED BEFORE FINAL IMPLEMENTATION.**

The existing specifications contain multiple references to randomness: deck generation, cut, random burn, commitment generation, and player participation. These must be separated into explicit domains.

At minimum:

1. **Shuffle randomness:** determines the cryptographic deck/order under the selected shuffle engine.
2. **Dealer consumption rules:** consume the already committed deck/state and must not silently create a competing shuffle.
3. **Commitment nonce randomness:** protects commitment hiding and is not the source of deck randomness.
4. **Protocol-selection randomness, if any:** must be separately specified and committed before it can affect the hand.

No implementation may use a predictable commitment hash as a substitute for secure shuffle randomness.

## 8. Finding E — replay boundary

**Status: OPEN / MUST BE RESOLVED.**

A replay must reproduce the canonical hand state from recorded inputs, selected engine identifier/version, commitments, proofs, and authorized transitions. Replay must never ask the system to regenerate private randomness unless the required seed/material is explicitly part of the replay specification.

## 9. Finding F — Request & Permission boundary

**Status: REQUIRES ALIGNMENT.**

The Request & Permission Engine may authorize engine selection, fallback, reveal requests, and inter-engine operations. It must not become the owner of cryptographic randomness, card assignment, or private-card plaintext.

The permission layer validates the transition; the domain engine performs the cryptographic operation.

## 10. Finding G — ledger boundary

**Status: CORRECTED.**

Engine 04 records evidence of shuffle selection, commitments, proofs, state transitions, reveals, failures, and replay identifiers. It must not become the source of private-card truth or a second card-distribution engine.

Private card plaintext should remain outside the general ledger unless a later protocol rule explicitly requires publication.

## 11. Required integration invariant

The complete card path should converge to one canonical state:

`Shuffle Engine → Card Assignment Contract → Engine 06 → Gameplay/Reveal → Engine 04 Evidence`

with Request & Permission controlling authorized transitions between engines.

The architecture therefore permits two implementations while maintaining one authoritative result per hand.
