# 06 — Commitment and Reveal Card Dealing Engine

**Chain Poker Genesis by LAEV**  
**Engine:** Commitment and Reveal Card Dealing Engine  
**Version:** 1.0 reconstruction  
**Historical source:** 6.0 Commitment and Reveal Card Dealing Engine__.pdf  
**Protocol author and designer:** Lerry Alexander Elizondo Villalobos (LAEV)

> Private card distribution, cryptographic commitment, encrypted player-card access, authorized reveal, and deterministic verification.

## 1. Purpose

Engine 06 defines the protocol boundary for private card assignment and later cryptographic revelation.

Its central security property is:

> A player may privately obtain and use their cards while other participants cannot derive the card values from the published commitment, and a later reveal can be checked against the commitment.

The engine does not itself define poker rules, monetary settlement, or the graphical presentation of the table.

## 2. Critical cryptographic distinction

The historical document combines several concepts that must be separated in implementation:

- **Commitment:** binds a card set to a cryptographic value without publishing the card values.
- **Encryption:** protects the actual private card payload while it is stored or transported.
- **Digital signature:** authorizes an action and binds it to a wallet/key.
- **Reveal:** publishes sufficient material to recompute and verify the commitment.

Therefore:

`signature ≠ encryption ≠ commitment`

A valid implementation must not assume that signing a commitment makes the cards confidential.

## 3. Recommended commitment model

For player `P`, hand `H`, canonical private cards `C`, and secret nonce `N`:

`commitment = H(protocol_id || hand_id || player_id || card_encoding || nonce)`

The exact hash algorithm, canonical encoding, domain separation, and nonce requirements must be fixed by the cryptographic specification before interoperability is claimed.

The nonce is essential because a commitment without adequate entropy can be vulnerable to guessing or dictionary attacks when the committed value comes from a small known card space.

## 4. Private card payload

The actual card material should be represented separately from the public commitment.

Conceptually:

`EncryptedCardPayload = AEAD_Encrypt(player_key, canonical_card_data, associated_data)`

Associated data should bind the ciphertext to the intended protocol context, such as:

- protocol identifier;
- table identifier;
- hand identifier;
- player identifier;
- commitment identifier;
- protocol version.

The precise encryption algorithm and key-management model require a dedicated cryptographic specification.

## 5. Player ownership and authorization

The player's wallet/key is used to authorize protocol actions.

At minimum, signatures may be required for:

- card commitment acceptance;
- reveal authorization;
- protocol requests associated with the player's private state.

A signature proves authorization by the corresponding key. It does not by itself prove that the signer is the human identity represented by the player unless the protocol separately defines that identity relationship.

## 6. Lifecycle

### 6.1 Hand initialization

1. Create a unique hand identifier.
2. Establish the participating player set.
3. Obtain the protocol-defined randomness.
4. Generate or derive the private card assignment according to the Poker/Card Distribution rules.
5. Generate a cryptographically secure nonce for each commitment.
6. Canonically encode the private card data.
7. Calculate each player's commitment.
8. Encrypt each player's private card payload.
9. Obtain the required wallet signature.
10. Publish or distribute only the information permitted by the protocol.

### 6.2 Hidden gameplay state

During active gameplay:

- card values remain private;
- commitments may be public or available to authorized nodes according to protocol rules;
- encrypted card payloads may be stored or transported as defined by the network protocol;
- plaintext private cards must not be broadcast as protocol messages;
- other players must not receive sufficient information to derive another player's card values.

### 6.3 Private viewing

The Viewer Engine requests or obtains the player's encrypted payload.

The authorization layer verifies that the requesting key corresponds to the intended player context.

Decryption is then performed using the protocol-defined key mechanism.

The exact wallet-to-encryption-key relationship is **not** assumed here and requires a dedicated key-management specification.

### 6.4 Reveal

When poker rules require a reveal:

1. Poker Rules Engine identifies the required reveal.
2. Requests and Permissions Engine creates the formal reveal request.
3. Player wallet authorizes the reveal when player authorization is required.
4. The reveal package supplies the required card data and nonce.
5. The verifier reconstructs the canonical commitment.
6. The reconstructed value is compared with the original commitment.
7. The reveal is accepted only if all required protocol conditions pass.
8. Accepted cards become public game state.

## 7. Reveal package

A minimum conceptual reveal package is:

`{hand_id, player_id, commitment_id, card_data, nonce, authorization_signature}`

The final wire format must define:

- serialization;
- encoding;
- signature format;
- hash algorithm;
- domain separation;
- version;
- error codes;
- replay protection.

## 8. Verification

Verification must independently establish:

1. the reveal belongs to the correct hand;
2. the player identifier matches;
3. the commitment identifier matches;
4. the canonical card encoding is valid;
5. the nonce is validly encoded;
6. the commitment recomputes to the stored value;
7. the signature, where required, is valid;
8. the reveal is authorized by the current poker state;
9. the reveal has not already been accepted or rejected under an incompatible state transition.

A commitment mismatch causes rejection.

## 9. Replay protection

Reveal requests and authorizations must be bound to a unique protocol context.

At minimum, implementations should prevent reuse across:

- different hands;
- different players;
- different commitment identifiers;
- incompatible protocol versions.

The exact anti-replay mechanism belongs to the Requests and Permissions Engine and cryptographic protocol specification.

## 10. Card-generation boundary

Engine 06 should not silently define the entire randomness/deck-generation protocol.

It consumes card-assignment output from the protocol's card-generation/randomness mechanism and converts that private state into commitments and protected payloads.

If the protocol requires multi-party randomness, deck cuts, burn-card randomness, or deterministic replay, those mechanisms must be specified in their corresponding engine.

## 11. Interaction with Engine 04

Engine 04 — Private Off-Chain Ledger Engine should record the cryptographic lifecycle without exposing private card plaintext unnecessarily.

Suitable event classes include:

- `CARD_COMMITMENT_CREATED`
- `CARD_PAYLOAD_PROTECTED`
- `CARD_REVEAL_REQUESTED`
- `CARD_REVEAL_AUTHORIZED`
- `CARD_REVEAL_ACCEPTED`
- `CARD_REVEAL_REJECTED`

The ledger should record commitments, hashes, identifiers, signatures and state transitions according to the privacy policy. Plaintext private cards should not be written into the general replicated ledger merely for auditability.

## 12. Interaction with Engine 03

The Cryptographic Connection Engine is responsible for the cryptographic connection/session layer defined by its own specification.

Engine 06 consumes the cryptographic identity and authorization mechanisms exposed by that layer; it does not redefine wallet connection semantics.

## 13. Interaction with Engine 02

The Graphical Interface Engine may expose:

- private-card viewing through the dedicated Viewer Engine;
- reveal status;
- commitment status;
- verification status;
- protocol errors.

It must not become the authority that decides whether a reveal is legal.

## 14. Security properties

The intended properties are:

- confidentiality of private cards before authorized reveal;
- binding of card data to a commitment;
- detection of card modification;
- authorization of player-controlled actions;
- prevention of unauthorized reveal acceptance;
- replay resistance;
- independently verifiable reveal.

These are protocol goals. They are not claims that every implementation automatically satisfies them.

## 15. Failure conditions

An implementation should reject the operation when:

- commitment is malformed;
- commitment does not match the revealed data;
- player identity does not match;
- hand context does not match;
- signature is invalid;
- reveal is not permitted by poker state;
- authorization is expired or already consumed;
- replay protection fails;
- required cryptographic parameters are unsupported.

## 16. Implementation status

This repository document is an implementation-facing reconstruction of the supplied historical specification.

The following remain to be formally specified before production interoperability:

- exact hash algorithm;
- exact canonical serialization;
- exact nonce length and generation;
- exact encryption algorithm;
- key derivation and encryption-key custody;
- wallet-signature algorithm;
- exact reveal wire format;
- randomness/deck-generation protocol;
- multi-party entropy protocol, if required;
- Viewer Engine interface;
- Requests and Permissions Engine interface;
- cryptographic error codes;
- formal threat model;
- test vectors.

These details must not be invented implicitly by individual implementations.

## 17. Source record

The supplied PDF remains the historical source of the Engine 06 requirements.

This README separates those historical requirements from implementation details that require later formalization.

---

© 2026 Lerry Alexander Elizondo Villalobos (LAEV).  
Chain Poker Genesis by LAEV.


## 18. Dual shuffle/distribution compatibility

Engine 06 is deliberately agnostic to the selected card-shuffle/distribution implementation.

The protocol may select one of two compatible mechanisms:

- **Engine A:** native Chain Poker Genesis shuffle/distribution mechanism;
- **Engine B:** independent verifiable-shuffle / mental-poker adapter.

Only one mechanism is authoritative for a hand. Engine 06 receives the canonical Card Assignment Result and does not choose between competing card assignments.

The selected shuffle engine identifier, version, assignment commitment and verification material become part of the hand context used by Engine 06.

Where the non-authoritative engine can independently verify the same canonical result, its verification may be recorded without changing the authoritative result.

A shuffle-engine change after authoritative commitment is forbidden. A failure before finalization must follow the protocol's explicit fallback/recovery state.

This preserves a single canonical hand state while avoiding dependence on one shuffle implementation.
