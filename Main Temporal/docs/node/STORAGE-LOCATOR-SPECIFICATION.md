# Node Core Storage Locator Specification

Project: Chain Poker Genesis by LAEV
Layer: Node Core
Version: 0.1.0
Status: Implementation baseline

## Purpose

The Storage Locator resolves a logical object identity to an authorized storage location.

```text
OBJECT_ID
  ↓
OBJECT REGISTRY
  ↓
LOGICAL PATH
  ↓
PROVIDER
  ↓
PHYSICAL / DISTRIBUTED LOCATION
```

## Location states

- LOCAL_ONLY
- DISTRIBUTED_ONLY
- LOCAL_AND_DISTRIBUTED
- SYNC_PENDING
- SYNC_PROCESSING
- MISSING_LOCAL
- MISSING_DISTRIBUTED
- CONFLICT
- QUARANTINED

The current baseline may produce LOCAL_ONLY. Distributed states remain reserved for future provider implementations.

## Safety

Normal reads must resolve through the registry and canonical path rules. Arbitrary filesystem scanning is not a normal location-resolution mechanism.