# Security — Rake Engine and Monetary Settlement Flow

## Security boundary

The engine handles accounting instructions and settlement-critical data. It must not expose private keys through:

- ledger records;
- JSON event payloads;
- logs;
- Merkle leaves;
- API responses;
- documentation examples.

## Required controls

### Deterministic calculation
Use integer satoshis for monetary arithmetic in the implementation. Avoid floating-point BTC calculations.

### Idempotent settlement
A unique rake event must map to one canonical settlement obligation. Retries must reference the same obligation rather than create a new one.

### Destination authorization
Foundation and AkaMoto Rie L destination addresses must be explicitly authorized by the active protocol configuration. Address changes require versioned governance/audit records.

### Transaction verification
A settlement should not be marked final solely because a transaction was broadcast. The implementation must distinguish:

- created;
- broadcast;
- observed;
- confirmed;
- failed/replaced.

### Ledger integrity
The Private Off-Chain Ledger should preserve the complete event chain and its Merkle/anchoring evidence.

### Failure recovery
A failed or delayed settlement must remain recoverable without duplicating the financial obligation.

## Threats to model

- duplicate rake calculation;
- duplicate settlement;
- manipulated pot amount;
- unauthorized destination address;
- compromised settlement signer;
- stale protocol configuration;
- transaction replacement;
- chain reorganization;
- operational-wallet compromise;
- ledger tampering;
- incorrect rounding;
- fee underfunding;
- replay of historical settlement requests.

## External-provider risk

The protocol boundary ends at the configured transfer to the external AkaMoto Rie L destination. Risks after receipt belong to the external company's operational, legal and financial controls and are not resolved by the Rake Engine.

## Security status

This document describes required security properties. It is not a security audit or formal verification report.
