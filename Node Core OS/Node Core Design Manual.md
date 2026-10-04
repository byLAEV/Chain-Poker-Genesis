# Node Core Design Manual

## Design Manual for Node Core OS

### Purpose

The **Node Core Design Manual** is the living design document for **Node Core OS**.

Its purpose is to progressively document the complete design, architecture, implementation model, and structural decisions of Node Core OS.

This manual is developed step by step. Each new design decision should be documented here so that the relationship between the architecture and its implementation remains clear and traceable.

# Design Implementation

## 1. Node Core OS

Node Core OS is the infrastructure layer that organizes the Node Core BIOS, Node Core, and the protocols installed over the Node Core.

### 1.1 Node Core BIOS

The **Node Core BIOS** is the infrastructure firmware layer responsible for boot, configuration, verification, storage, content resolution, materialization, recovery, and controlled activation of the Node Core.

### 1.2 Node Core

The **Node Core** is the protocol-neutral core and runtime of the node.

It provides the common infrastructure required by installed protocols while remaining separate from protocol-specific logic.

### 1.3 Protocols

The **Protocols** layer contains protocol implementations installed over the Node Core.

Chain Poker Genesis belongs to this layer and must remain architecturally separated from the Node Core infrastructure.

# Design Development Record

This document is a living record of the Node Core OS design.

The design will be expanded progressively as each architectural component is defined, normalized, canonicalized, specified, tested, and implemented.

New sections should document the design in sequence rather than silently replacing previously established architectural decisions.
