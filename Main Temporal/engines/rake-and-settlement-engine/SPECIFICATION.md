# Rake Engine and Monetary Settlement Flow — Specification

**Protocol:** Chain Poker Genesis by LAEV (peroqtdigo)  
**Version:** 1.0  
**Document:** 5.0  
**Status:** NORMAL / SPECIFICATION

## 1. Scope

The Rake Engine is responsible for deterministic calculation and recording of poker-table rake. The Monetary Settlement Engine is responsible for final distribution of the accumulated rake.

This document separates those responsibilities while preserving the behavior stated in the source specification.

## 2. Inputs

A rake calculation requires, at minimum:

- table identifier;
- hand identifier;
- completed-hand state;
- eligible pot value;
- protocol version;
- configured rake percentage;
- operational-wallet context;
- ledger context.

## 3. Default parameters

- Game: Texas Hold'em Cash Game.
- Protocol version: 1.0.
- Rake percentage: 3%.
- Foundation share of rake: 11%.
- AkaMoto Rie L share of rake: 89%.

The source specification calls this a standard fixed-industry rake model, but this document does not add a cap, minimum, rounding rule, eligibility threshold or jurisdiction-specific rule that was not supplied in the source.

## 4. Calculation

For an eligible pot (P):

`rake = P × 0.03`

`players_pot = P - rake`

For the rake amount (R):

`foundation = R × 0.11`

`akamoto = R × 0.89`

Therefore:

`foundation + akamoto = rake`

### Examples

| Pot | Rake | Players' pot | Foundation | AkaMoto Rie L |
|---:|---:|---:|---:|---:|
| 0.01000000 BTC | 0.00030000 BTC | 0.00970000 BTC | 0.00003300 BTC | 0.00026700 BTC |
| 0.50000000 BTC | 0.01500000 BTC | 0.48500000 BTC | 0.00165000 BTC | 0.01335000 BTC |
| 1.00000000 BTC | 0.03000000 BTC | 0.97000000 BTC | 0.00330000 BTC | 0.02670000 BTC |

## 5. State flow

`HAND_COMPLETED`
→ `RAKE_ELIGIBILITY_EVALUATED`
→ `RAKE_CALCULATED`
→ `RAKE_RECORDED`
→ `RAKE_MOVED_TO_TABLE_OPERATIONAL_WALLET`
→ `SETTLEMENT_REQUESTED`
→ `SETTLEMENT_EXECUTED`
→ `DESTINATIONS_RECORDED`
→ `SETTLEMENT_CONFIRMED`

Failure states should preserve the original event and prevent silent loss or duplication.

## 6. Idempotency

A settlement implementation must not pay the same rake obligation twice.

A suitable implementation-level identity should bind at least:

- protocol version;
- table identifier;
- hand identifier;
- rake event identifier;
- source operational wallet;
- destination allocation;
- settlement attempt.

The exact identifier format is an implementation decision and must be documented before production use.

## 7. Ledger record

The source specification requires an auditable record containing:

- table identifier;
- hand identifier;
- timestamp;
- pot value;
- rake amount;
- source wallet address;
- destination wallet address;
- transaction hash;
- JSON record;
- Merkle-tree inclusion;
- anchoring information.

The ledger is evidence of the event history. It does not by itself constitute proof that an external company is licensed or compliant.

## 8. Monetary settlement

The Monetary Settlement Engine receives the accumulated rake from the table operational wallet and performs the configured allocation:

- 11% → Foundation wallet;
- 89% → one Bitcoin wallet owned/controlled by AkaMoto Rie L.

The source specification explicitly states that the 89% allocation is not split by Chain Poker Genesis between multiple AkaMoto wallets.

## 9. Asset separation

The intended accounting boundary is:

`Chain Poker Genesis → 11% Foundation`

and

`Chain Poker Genesis → 89% AkaMoto Rie L`

The specification requires no commingling between these destinations at the protocol accounting layer.

## 10. External-company boundary

AkaMoto Rie L is defined by the source document as a private company external to the protocol. Its stated responsibilities include:

- maintaining operational BTC reserves;
- converting BTC to fiat;
- charging commercial service fees;
- liquidity management;
- operational risk management;
- applicable accounting, tax and regulatory obligations.

The protocol does not specify the company's internal accounting or treasury implementation.

## 11. Rounding and Bitcoin precision

The source document provides BTC examples to eight decimal places but does not define:

- integer-satoshi calculation requirements;
- rounding direction;
- dust handling;
- minimum settlement amount;
- aggregation threshold;
- fee payer;
- network-fee accounting.

These are **specification gaps** that must be resolved before a production implementation can be considered deterministic.

## 12. Rake eligibility

The source document refers to an “eligible pot” but does not define the complete eligibility rule.

A future normative rule set should specify:

- whether every completed cash-game hand is eligible;
- treatment of split pots;
- side pots;
- all-in pots;
- uncalled bets;
- zero-rake hands;
- disconnected players;
- aborted hands;
- protocol faults.

Until defined, implementations must not invent these rules and call them protocol behavior.

## 13. Settlement fees

The source document requires verifiable Bitcoin transfers but does not specify whether Bitcoin network fees:

- are paid by the operational wallet;
- are deducted from the rake;
- are charged separately;
- are allocated between destinations;
- are covered by AkaMoto Rie L after receipt.

This must be defined before production settlement.

## 14. Security invariants

An implementation should enforce:

1. rake cannot exceed the eligible pot;
2. allocation percentages must sum to 100% of the rake;
3. a completed hand produces at most one canonical rake obligation;
4. a settled obligation cannot be settled again;
5. destination changes are version-controlled and auditable;
6. private keys are never stored in the ledger;
7. transaction hashes are recorded only after the relevant transaction exists;
8. ledger records are append-oriented and tamper-evident;
9. settlement failures remain recoverable without creating duplicate payments.

## 15. Normative boundary

This specification defines the intended protocol behavior contained in document 5.0. It does not independently establish:

- legal classification of poker activity;
- gambling authorization;
- money-transmission authorization;
- Bitcoin-to-fiat licensing;
- tax treatment;
- AML/KYC obligations;
- legality of operating in any particular jurisdiction.

Those matters require jurisdiction-specific legal and compliance analysis.

## 16. Open specification items

Before implementation, resolve:

- rake caps and/or minimums;
- eligibility rules;
- satoshi-level rounding;
- Bitcoin network-fee treatment;
- settlement batching;
- confirmation policy;
- reorg handling;
- failed transaction recovery;
- destination-wallet rotation;
- authorization for settlement;
- emergency pause behavior;
- version activation rules;
- reconciliation between ledger totals and on-chain settlement.

## 17. Definition

The Rake Engine calculates and records the configured 3% rake for eligible Texas Hold'em Cash Game pots. The Monetary Settlement Engine subsequently distributes that rake according to the protocol configuration: 11% to the Foundation and 89% to the designated AkaMoto Rie L Bitcoin wallet, with an auditable record linking the hand, calculation, wallets and settlement transaction.
