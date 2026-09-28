# Engine 05 — Functional Specification

## 1. Functional contract

Input: authorized completed-hand state plus the protocol's configured rake parameters.

Output: one canonical rake obligation and, when authorized, a settlement request.

## 2. Formula

For eligible pot P:

R = P × 0.03
F = R × 0.11
A = R × 0.89

Invariant: F + A = R.

The final production representation must operate in integer satoshis once the rounding policy is formally defined.

## 3. State machine

HAND_COMPLETED → ELIGIBILITY_CHECK → CALCULATED → OBLIGATION_CREATED → SETTLEMENT_REQUESTED → SETTLED

Failure paths:
ELIGIBILITY_CHECK → INELIGIBLE
SETTLEMENT_REQUESTED → SETTLEMENT_FAILED

A failed settlement must not erase the obligation.

## 4. Authority model

| Decision | Owning component |
|---|---|
| Whether the hand is complete | Poker Rules / protocol state |
| Whether the pot is rake-eligible | Engine 05 |
| Rake calculation | Engine 05 |
| Player/table permission | Requests & Permissions |
| Operational wallet state | Table Wallet Engine |
| Final Bitcoin transfer | Monetary Settlement Engine |
| Historical evidence | Private Off-Chain Ledger Engine |
| Card privacy/reveal | Engine 06 |

## 5. Event contract

Engine 05 emits structured events consumed by Engine 04. Each event requires an event identifier, protocol version, table identifier, hand identifier, engine identifier, event type, canonical payload and protocol timestamp.

## 6. Idempotency contract

The canonical obligation must be uniquely addressable. Repeated processing of the same completed-hand event must return the existing obligation rather than create a second obligation. Settlement retries must reference the same obligation.

## 7. Precision contract

Until a formal precision specification exists, no implementation may claim full deterministic compatibility merely from the percentage formulas.

Required future definitions: integer-satoshi conversion, rounding mode, minimum amount, dust policy and fee accounting.

## 8. Settlement handoff

Conceptual request:

SettlementRequest {
  obligation_id
  table_id
  hand_id
  source_wallet_context
  destinations
  amounts
  authorization_context
}

The settlement engine returns a transaction result that is recorded by Engine 04.

## 9. Reconciliation

A completed settlement must be reconcilable across:

Hand → RakeObligation → SettlementRequest → Bitcoin Transaction → Ledger Record

Any broken link is an audit exception.

## 10. Compatibility rule

Implementations are compatible only when identical canonical inputs and the same declared protocol parameters produce identical obligation results.
