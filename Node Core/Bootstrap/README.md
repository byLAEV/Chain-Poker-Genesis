# Node Core Bootstrap

Status: IMPLEMENTED
Version: 1.0.0

Bootstrap is the fixed, protocol-neutral installation boundary for Node Core.

Responsibilities:
- create the minimum Node Core filesystem;
- initialize local bootstrap metadata;
- verify installation invariants;
- recover incomplete bootstrap;
- report Node Core readiness.

Bootstrap does not generate cryptographic identities, create private keys, install CPG, create a CPG ledger, select a protocol, install protocol engines, or manage decentralized storage providers.

Flow:
Installer -> Initialization -> Verification -> Node Core Ready

Interrupted installation:
Recovery -> Verification -> Node Core Ready

The installer is fixed. Protocol engines and later components are installed independently.
