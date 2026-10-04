# Node Manager

**Status:** SUPPORTING / RECONCILED  
**Implementation:** IMPLEMENTED_PARTIAL

The Node Manager is the Node Core control-plane coordinator.

## Canonical authority

The normative contract is:

`Documentation/Interfaces/NODE-MANAGER-CONTRACT.md`

The Node Manager does not redefine subsystem lifecycles.

## Boundaries

```
Node Manager
   ├── Configuration Manager → configuration
   ├── Runtime Manager       → Node Core runtime lifecycle
   ├── Engine Runtime        → engine lifecycle
   ├── Protocol Interface    → protocol installation boundary
   └── Recovery              → recovery execution
```

Node Manager coordinates these services; it does not replace them.

## Canonical operations

- status / snapshot
- readiness
- initialize
- start
- stop
- recover
- register_engine
- unregister_engine
- request_protocol_installation

## Invariants

- Configuration is required before Node Manager reaches READY.
- Failed Runtime readiness cannot produce READY.
- Engine registration is delegated to Engine Runtime.
- Protocol installation is delegated to Protocol Interface.
- Recovery is delegated to Recovery.
- CPG ledger, consensus, poker rules, Table Wallet and settlement are outside this component.
- Management events are retained as an auditable control-plane record.

The manifest remains authoritative for implementation availability.
