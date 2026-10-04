# Node Core CLI

**Status:** IMPLEMENTED_PARTIAL / RECONCILED
**Version:** 1.0.0

The CLI is a thin operator boundary over Node Manager.

Canonical commands:
- `node status`
- `node readiness`
- `node start`
- `node stop`
- `node recover`

The CLI does not own lifecycle state. It delegates to Node Manager and returns deterministic compact JSON for successful operations and structured JSON errors for operational failures.

It does not expose CPG-specific commands, table state, Table Wallet, settlement, rake, ledger mutation or protocol consensus.

Parser-level argument errors remain the standard argparse non-zero failure path defined by the canonical CLI contract.


## Operator menu entry point

The canonical interactive entry point is `node_core_menu.py`. It creates the
Node Core composition and passes it to the existing CLI boundary.

From a Termux installation:

```sh
python ~/.chain-poker-genesis/node-core/CLI/node_core_menu.py
```

The installed Node Core directory can also be selected explicitly with
`NODE_CORE_ROOT`.

The entry point does not install, update, or overwrite Node Core. It only
starts the operator interface for an existing installation.
