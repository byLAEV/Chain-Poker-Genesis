# Node Core Time Service Contract

**Status:** Normative design baseline  
**Scope:** Protocol-neutral Node Core

## Purpose
Provide a deterministic time-service boundary for timestamps, ordering metadata, validation, and future synchronization without making wall-clock time an unquestioned consensus truth.

## Time domains
- system time;
- external reference time;
- network-observed time;
- reference epoch;
- logical/sequential time.

## Required operations
- `now()`
- `timestamp()`
- `validate_timestamp()`
- `reference_status()`
- `logical_tick()`

## Rules
1. Every timestamp has an explicit format and unit.
2. Invalid or ambiguous timestamps MUST be rejected.
3. System clock time is an observation, not automatically a consensus authority.
4. External/network references must be identified and their trust state exposed.
5. Logical ordering must remain available when wall-clock confidence is insufficient.
6. Time synchronization MUST NOT be implemented as network consensus until its protocol is formally specified.
7. CPG-specific time semantics do not belong to Node Core.

## Non-goals
No CPG table timing, betting timers, block-time assumptions, or protocol-specific consensus rules are defined here.
