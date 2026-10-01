# Canonical Field Registry — Reconciliation Draft

Protocol: Chain Poker Genesis by LAEV
Revision: 0.1.0
Status: Reconciliation draft — not yet normative

This registry is the authority layer between audited engine specifications and JSON Schemas.

## Rules
1. A field is canonical only when its semantic owner is identified.
2. A field appearing in more than one engine must have one protocol meaning and explicit ownership.
3. Similar names are not merged automatically.
4. Hash fields remain opaque until canonical serialization and cryptographic profiles are accepted.
5. Event fields are governed by Engine 04 until the cross-engine event model is reconciled.
6. State fields are provisional until the integrated state machine is accepted.

## Identity / Node
| Canonical concept | Current name | Authority | Decision |
|---|---|---|---|
| Cryptographic identity reference | identity_id | Cryptographic Connection | Keep |
| Node identity reference | node_id | Player Node / Ledger source | Keep; do not merge with identity_id |
| Player identity reference | player_id | Table Join boundary | Keep distinct; reconcile identity relationship |
| Credential method | credential_type | Cryptographic Connection | Keep |
| Public verification key | public_key | Cryptographic Profile | Provisional |
| Signature profile | signature_scheme | Cryptographic Profile | Provisional |

## Table
| Canonical concept | Current name | Authority | Decision |
|---|---|---|---|
| Table identity | table_id | Table Creation | Keep |
| Creation commitment | creation_hash | Table Creation | Keep |
| Configuration commitment | configuration_hash | Table Creation | Keep; define scope |
| Initial state commitment | initial_state_hash | Table Creation | Keep |
| Table lifecycle | lifecycle_state | Table Creation / lifecycle | Keep provisionally |
| Protocol version | protocol_version | Protocol | Keep |
| Rules version | rules_version | Poker Rules | Keep |
| Card engine binding | selected_card_engine_id/version | Table Creation + Card Engine | Keep |
| Table wallet reference | table_wallet_reference | Table Wallet boundary | Keep provisionally |

## Participant
| Canonical concept | Current name | Authority | Decision |
|---|---|---|---|
| Table-scoped participant identity | table_participant_id | Table Join | Keep provisionally |
| Player identity | player_id | Table Join / identity boundary | Keep distinct from node_id |
| Player node | player_node_id | Player Node | Keep |
| Seat | seat_id | Table Join / Poker Rules | Keep |
| Participation lifecycle | participant_status | Table Join / Disconnection | Keep |
| Wallet identity | wallet_id | Table Wallet | Provisional |
| Wallet address | wallet_address | Settlement/Wallet | Open |
| Wallet network | wallet_network | Settlement/Wallet | Open |
| Wallet currency | wallet_currency | Settlement/Wallet | Open |

## Hand
| Canonical concept | Current name | Authority | Decision |
|---|---|---|---|
| Hand identity | hand_id | Poker lifecycle | Keep |
| Participant-set commitment | participant_set_hash | Hand context | Provisional |
| Table configuration commitment | table_configuration_hash | Table Creation | Keep |
| Card engine binding | card_engine_id/version | Card Engine | Keep |
| Commitment version | commitment_version | Commitment & Reveal | Keep |
| Dealer version | dealer_version | Dealer | Provisional |
| Randomness commitment | randomness_commitment | Commitment/Card Engine | Keep provisionally |
| Previous state reference | previous_state_id | State Machine | Open |
| Current state commitment | state_hash | State Machine | Open |
| Hand lifecycle | hand_status | Poker Rules | Provisional |

## Event — authoritative baseline
Engine 04 currently defines the event-model candidates: event_id, timestamp, node_id, session_id, game_id, hand_id, engine_id, event_type, event_version, payload, previous_hash, event_hash, merkle_batch_id, anchor_status, bitcoin_anchor_id.

The following fields from the first event schema are not yet canonical equivalents: actor_id, scope_id, sequence, previous_event_id, payload_hash, state_hash, signature, visibility.

They may eventually be derived, renamed, or retained as separate fields, but no equivalence should be assumed.

## Critical distinctions
`identity_id != node_id != player_id`

`configuration_hash != state_hash != event_hash != previous_hash`

These identities and commitments have different semantic roles and must not be collapsed into generic identifiers or hashes.

## Next reconciliation
The next audit must map Engine 04 event fields to the Table, Participant, Hand, Node and Identity objects and determine which event fields are required, conditional, derived, private, serialized, hashed, scope-defining, causality-defining, or ledger-only.

Only after that mapping should event.schema.json be rewritten.