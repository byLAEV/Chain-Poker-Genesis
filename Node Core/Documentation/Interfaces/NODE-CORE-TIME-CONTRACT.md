# Node Core Time Contract

**Status:** CANONICAL  
**Version:** 1.0.0  
**Scope:** Protocol-neutral local and logical time service

## 1. Purpose

Time provides timestamp observation, validation, logical ordering and integrity-linked sequential records.

System clock time is an observation. It is not automatically a consensus authority.

## 2. Canonical operations

- `now()`
- `timestamp(value)`
- `validate_timestamp(value)`
- `reference_status()`
- `logical_tick()`
- `record(timestamp)`

## 3. Timestamp contract

Reference timestamps use integer Unix seconds.

Invalid types and negative timestamps MUST be rejected.

## 4. Logical ordering

Logical sequence numbers MUST increase monotonically within a Time Service instance.

Logical ordering MUST remain available independently of wall-clock confidence.

## 5. Integrity records

Each record contains:

- sequence;
- timestamp;
- previous_hash;
- record_hash.

`record_hash` is SHA-256 over the canonical JSON representation of sequence, timestamp and previous_hash.

The first record has `previous_hash = null`.

Each subsequent record MUST reference the immediately preceding record hash.

## 6. Determinism

Given identical sequence, timestamp and previous_hash inputs, record hashing MUST produce the same digest.

Serialization uses sorted keys and deterministic separators.

## 7. Runtime dependency

Time is a supporting Node Core service.

Node Core Runtime readiness MUST NOT depend on wall-clock synchronization.

Runtime may use Time for lifecycle records or future observability, but Time MUST NOT independently authorize Runtime state transitions.

## 8. Network boundary

Network-observed or external time references require an explicit trust model.

Network connectivity MUST NOT convert local time into consensus time.

## 9. Protocol isolation

CPG table timers, betting clocks, block-time assumptions and protocol-specific temporal consensus are outside this contract.

## 10. Implementation status

The Time manifest declares `IMPLEMENTED_PARTIAL`.

Implemented baseline:

- local reference clock;
- timestamp generation;
- timestamp validation;
- sequential records;
- hash-chain integrity;
- local reference status.

Network time consensus remains unimplemented by design.

## 11. Verification

Tests MUST verify:

1. timestamp validity;
2. monotonic sequence;
3. first-record null predecessor;
4. correct predecessor linkage;
5. deterministic hashing;
6. broken-chain detection;
7. local clock is not consensus authority;
8. Runtime does not require network time consensus.
