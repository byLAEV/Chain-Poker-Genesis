# Canonical Schema Audit — Field Authority Registry

Protocol: Chain Poker Genesis by LAEV
Revision: 0.1.0
Status: Active audit

Purpose: trace every canonical field to an audited architectural source before the field becomes normative.

## Audit rule
A field is not protocol-canonical merely because it appears in a JSON Schema.

Each field requires: source authority; owning engine/domain; semantic class; mutability; privacy; hash/serialization status; replay relevance; specification status.

Status vocabulary:
- AUDITED = explicitly established by an audited repository specification.
- INFERRED = strongly implied by audited architecture but not explicitly frozen.
- OPEN = the concept exists, but its exact technical definition remains open.
- PROVISIONAL = currently represented in the schema but requires reconciliation.

## Identity
| Field | Owner | Class | Privacy | Replay | Status |
|---|---|---|---|---|---|
| identity_id | Cryptographic Connection | identity | public reference | yes | INFERRED |
| identity_version | Cryptographic Connection | version | public | yes | INFERRED |
| identity_status | Cryptographic Connection | lifecycle | public | yes | AUDITED |
| credential_type | Cryptographic Connection | credential metadata | public | yes | AUDITED |
| public_key | Cryptographic Connection | cryptographic identity | public | yes | OPEN |
| signature_scheme | Cryptographic Connection | cryptographic profile | public | yes | OPEN |
| key_reference | Cryptographic Connection | key reference | public reference | yes | OPEN |

Private keys, seed material and seed phrases are credential inputs and must never become canonical protocol-state fields.

## Node
| Field | Owner | Class | Privacy | Replay | Status |
|---|---|---|---|---|---|
| node_id | Node / Cryptographic Connection | identity reference | public | yes | INFERRED |
| node_version | Node architecture | version | public | yes | INFERRED |
| node_status | Player Node Disconnection Management | lifecycle state | public | yes | AUDITED |
| identity_id | Cryptographic Connection | identity reference | public | yes | AUDITED |
| protocol_version | Protocol | execution context | public | yes | AUDITED |
| capabilities | Node | capability metadata | public | yes | INFERRED |
| configuration_hash | Node/configuration | cryptographic commitment | public | yes | INFERRED |
| state_hash | Node state | state commitment | public | yes | INFERRED |

## Table
| Field | Owner | Class | Privacy | Replay | Status |
|---|---|---|---|---|---|
| table_id | Table Creation | identity | public | yes | AUDITED |
| creation_hash | Table Creation | creation commitment | public | yes | AUDITED |
| creation_timestamp | Table Creation | temporal metadata | public | yes | AUDITED |
| configuration_hash | Table Creation | configuration commitment | public | yes | AUDITED |
| initial_state_hash | Table Creation | state commitment | public | yes | AUDITED |
| lifecycle_state | Table/lifecycle authorities | state | public | yes | AUDITED |
| protocol_version | Protocol | execution context | public | yes | AUDITED |
| rules_version | Poker Rules | execution context | public | yes | AUDITED |
| game_variant | Table Creation/Poker Rules | configuration | public | yes | AUDITED |
| player_capacity | Table Creation | configuration | public | yes | AUDITED |
| blind_configuration | Table Creation/Poker Rules | configuration | public | yes | AUDITED |
| betting_structure | Table Creation/Poker Rules | configuration | public | yes | AUDITED |
| currency_configuration | Table/Settlement boundary | configuration | public | yes | INFERRED |
| network_configuration | Table/Settlement boundary | configuration | public | yes | INFERRED |
| selected_card_engine_id | Table/Card Engine boundary | execution binding | public | yes | AUDITED |
| selected_card_engine_version | Table/Card Engine boundary | execution binding | public | yes | AUDITED |
| selected_crypto_engine_id | Cryptographic boundary | execution binding | public | yes | OPEN |
| table_wallet_reference | Table Wallet boundary | component reference | public reference | yes | AUDITED |

## Participant
| Field | Owner | Class | Privacy | Replay | Status |
|---|---|---|---|---|---|
| table_participant_id | Table Join | table-scoped identity | public | yes | INFERRED |
| table_id | Table | scope reference | public | yes | AUDITED |
| player_id | Player/identity boundary | participant identity | public | yes | AUDITED |
| player_node_id | Player Node | node reference | public | yes | AUDITED |
| wallet_id | Table Wallet/participant | financial reference | controlled | yes | INFERRED |
| wallet_address | Settlement/wallet | settlement reference | controlled | yes | OPEN |
| wallet_network | Settlement/wallet | network metadata | public | yes | OPEN |
| wallet_currency | Settlement/wallet | asset metadata | public | yes | OPEN |
| seat_id | Table Join/Poker Rules | seat allocation | public | yes | AUDITED |
| participant_status | Table Join/Disconnection | membership state | public | yes | AUDITED |
| protocol_version | Protocol | execution context | public | yes | AUDITED |

## Hand
| Field | Owner | Class | Privacy | Replay | Status |
|---|---|---|---|---|---|
| hand_id | Poker lifecycle | hand identity | public | yes | AUDITED |
| table_id | Table | scope reference | public | yes | AUDITED |
| protocol_version | Protocol | execution context | public | yes | AUDITED |
| rules_version | Poker Rules | execution context | public | yes | AUDITED |
| card_engine_id | Card Engine boundary | execution binding | public | yes | AUDITED |
| card_engine_version | Card Engine boundary | execution binding | public | yes | AUDITED |
| commitment_version | Commitment & Reveal | execution binding | public | yes | AUDITED |
| canonicalization_version | Canonicalization | serialization context | public | yes | OPEN |
| dealer_version | Dealer | execution binding | public | yes | INFERRED |
| participant_set_hash | Table/hand context | set commitment | public | yes | INFERRED |
| table_configuration_hash | Table Creation | configuration commitment | public | yes | AUDITED |
| randomness_commitment | Commitment/Card Engine | randomness commitment | public reference | yes | AUDITED |
| previous_state_id | State machine | state linkage | public | yes | INFERRED |
| state_hash | State machine | state commitment | public | yes | INFERRED |
| hand_status | Poker Rules | lifecycle state | public | yes | INFERRED |

## Event — critical reconciliation
Engine 04 explicitly establishes an event baseline containing: event_id, timestamp, node_id, session_id, game_id, hand_id, engine_id, event_type, event_version, payload, previous_hash, event_hash, merkle_batch_id, anchor_status, and bitcoin_anchor_id.

The current event.schema.json instead uses actor_id, scope_id, sequence, previous_event_id, payload_hash, state_hash, signature, and visibility.

Therefore event.schema.json is PROVISIONAL and must not be promoted to canonical status until it is reconciled with Engine 04.

## Cross-cutting rule
A field with a name ending in hash is not thereby assigned a specific hash algorithm, serialization boundary, or cryptographic profile. Until those specifications are frozen, hashes are opaque commitments/references.

## Immediate corrections identified
1. Reconcile event.schema.json with Engine 04.
2. Treat canonicalization_version as an unresolved dependency until Canonical Serialization is defined.
3. Keep selected_crypto_engine_id provisional.
4. Keep wallet_address, wallet_network and wallet_currency open until Table Wallet/Settlement authority is reconciled.
5. Keep public_key and signature_scheme open pending the Cryptographic Profile.
6. Keep state_hash and previous_state_id provisional pending the Integrated State Machine.
7. Keep capabilities provisional pending a node capability specification.

## Next gate
Do not add more schemas yet.

First reconcile the Identity, Node, Table, Participant and Hand registries with Engine 04's Event Model. Then derive the definitive Canonical Field Registry from that reconciliation.

Only after the registry is accepted should Canonical Serialization be frozen.