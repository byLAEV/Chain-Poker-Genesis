# Review Questions

## 1. Protocol determinism

- Are all deterministic inputs defined?
- Are canonical encodings defined?
- Are ordering rules complete?
- Are identical inputs guaranteed to produce identical outputs?
- Are randomness sources and their verification rules completely specified?

## 2. State machine

- Are all states defined?
- Are every valid transition and invalid transition defined?
- Are concurrent actions handled deterministically?
- Are timeout, cancellation, disconnect, and recovery states specified?

## 3. Poker engine

- Are betting rounds, blinds, actions, side pots, showdown and hand evaluation completely deterministic?
- Can two independent implementations produce identical results?
- Is replay independent from presentation/UI?

## 4. Cryptography

- Are algorithms, curves, hash functions, encodings and signature formats normative?
- Are key-generation, custody, rotation, revocation and recovery requirements specified?
- Are cryptographic domain-separation rules defined?

## 5. Dealer / private cards

- Does the Commit-Reveal design prevent unilateral control?
- Is deck construction/shuffling independently verifiable?
- Are abort, non-reveal and malicious-participant cases specified?
- Are private-card proofs sufficient for the claimed properties?

## 6. CID / event logs

- Is CID generation canonical?
- Can events be fragmented and chained without ambiguity?
- Can a verifier reconstruct the complete event history?
- Are missing, duplicated, reordered and conflicting fragments detectable?

## 7. Ledger and replay

- Is the event schema canonical?
- Are hashes and Merkle structures precisely specified?
- Can historical state be reconstructed solely from valid protocol records?

## 8. P2P and synchronization

- Are message formats and transport assumptions defined?
- Are peer discovery, authentication, synchronization and conflict cases specified?
- What happens when nodes disagree or disappear?

## 9. Consensus

- What exactly constitutes valid consensus?
- What data is subject to consensus?
- Are thresholds, membership, timing and failure cases normative?

## 10. Settlement

- Are Bitcoin and Lightning settlement states separated from poker state?
- Are transaction authorization and settlement finality precisely defined?
- What happens when settlement is delayed or fails?

## 11. Security

- What are the explicit threat assumptions?
- Which attacks are in scope?
- Which guarantees are proven, tested, or only architectural goals?

## 12. Implementation

- Can two independent teams implement the protocol without private clarification from LAEV?
- Which interfaces must be frozen before implementation?
- Which components can evolve without changing the base protocol?
