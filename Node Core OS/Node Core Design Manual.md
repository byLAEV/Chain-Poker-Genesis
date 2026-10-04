# Node Core Design Manual

## Design Manual for Node Core OS

### Purpose

The **Node Core Design Manual** is the living design document for **Node Core OS**.

Its purpose is to progressively document the complete design, architecture, implementation model, and structural decisions of Node Core OS.

This manual is developed step by step. Each new design decision should be documented here so that the relationship between the architecture and its implementation remains clear and traceable.

# Design Implementation

## 1. Node Core OS

The design strategy for **Node Core OS** is to develop the node infrastructure through a **BIOS-oriented work format**.

For this reason, the architecture is organized into three distinct instances:

1. **Node Core BIOS**
2. **Node Core**
3. **Protocols**

In the repository, the main **Node Core OS** directory contains these three instances and the Node Core OS README.

The structure is:

```text
Node Core OS/
│
├── README.md
│
├── Node Core BIOS/
│   ├── BIOS-MANIFEST.json
│   ├── README.md
│   ├── Configuration/
│   ├── EAL/
│   ├── Boot/
│   ├── Storage/
│   ├── IPFS/
│   ├── Security/
│   ├── Materializer/
│   ├── Recovery/
│   └── UI/
│
├── Node Core/
│   ├── ...
│
└── Protocols/
    └── Chain Poker Genesis/
```

These three instances are architecturally related, but they have different responsibilities.

### 1.1 Node Core BIOS

The **Node Core BIOS** is the infrastructure firmware instance of Node Core OS.

It is responsible for the infrastructure operations required to initialize and manage the Node Core environment, including configuration, boot, verification, storage, IPFS/Kubo integration, security, materialization, recovery, and administrative interaction.

The BIOS is therefore designed as an independent infrastructure layer rather than as the Node Core itself.

Its internal design begins with:

- **BIOS-MANIFEST.json**
- **README.md**
- **Configuration/**
- **EAL/**
- **Boot/**
- **Storage/**
- **IPFS/**
- **Security/**
- **Materializer/**
- **Recovery/**
- **UI/**

### 1.2 Node Core

The **Node Core** is the protocol-neutral core and runtime instance of the node.

It provides the common infrastructure required by installed protocols while remaining separate from protocol-specific logic.

The Node Core is not the BIOS and is not itself a protocol. Its internal structure is developed independently within the Node Core instance.

### 1.3 Protocols

The **Protocols** instance contains protocol implementations installed over the Node Core.

**Chain Poker Genesis** belongs inside this layer.

This separation allows Chain Poker Genesis to be developed as a protocol over the Node Core infrastructure without merging protocol-specific responsibilities into the BIOS or the protocol-neutral Node Core.

# Design Development Record

This document is a living record of the Node Core OS design.

The design will be expanded progressively as each architectural component is defined, normalized, canonicalized, specified, tested, and implemented.

The BIOS-oriented work strategy establishes the initial architectural separation between **Node Core BIOS**, **Node Core**, and **Protocols**.

New design decisions should be documented here in sequence so that the evolution of the architecture remains explicit and traceable.
