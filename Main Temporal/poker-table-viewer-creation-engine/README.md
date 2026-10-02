# Poker Table Viewer Creation Engine

## Formal Architectural Specification

**Author:** Lerry Alexander Elizondo Villalobos — LAEV / byLAEV
**Author Identity:** LAEV
**Project:** Chain Poker Genesis by LAEV
**Component:** Poker Table Viewer Creation Engine
**Document Type:** Formal Technical Architecture Specification
**Status:** Architectural Definition
**Language:** English
**Version:** 1.0

***

## 1. Purpose

The **Poker Table Viewer Creation Engine** is a protocol component of **Chain Poker Genesis by LAEV** responsible for creating, configuring, generating, selecting, and binding visual table viewers to poker table instances.

The engine establishes a formal separation between:

1. the **poker protocol and table state**,
2. the **table identity and cryptographic verification**, and
3. the **visual representation of the table**.

The viewer is therefore treated as a presentation and binding component of the protocol rather than as the owner or source of the table itself.

The engine allows a participant to create a table viewer independently and later bind that viewer to a specific poker table.

The same viewer definition may therefore be used to represent multiple compatible tables, while a single table may be represented through different viewer definitions.

***

# 2. Architectural Principle

The central architectural principle is:

> **A poker table viewer defines how a table is presented; it does not define the table itself.**

The poker table remains an independent protocol object identified and verified through its table identity mechanisms.

The viewer obtains the identity of the table to which it is being connected through the protocol.

The relationship is therefore:

```text
TABLE PROTOCOL
      │
      ▼
TABLE IDENTITY
      │
      ├── Table Identifier
      └── Cryptographic Signature
      │
      ▼
VIEWER BINDING
      │
      ▼
VIEWER RENDERING
      │
      ▼
VISUAL TABLE
```

This architecture prevents the visual layer from becoming the authoritative source of table state.

***

# 3. Scope

The Poker Table Viewer Creation Engine is responsible for:

- viewer creation;
- viewer configuration;
- predefined viewer templates;
- custom viewer design;
- default viewer generation;
- image-based viewer configuration;
- code-based viewer generation;
- viewer format specifications;
- viewer storage and identification;
- viewer selection;
- runtime table binding;
- validation of table identity;
- cryptographic association with a table;
- visual rendering of protocol table state.

The engine does not replace the poker protocol, ledger, table state machine, settlement layer, wallet layer, or consensus mechanisms.

***

# 4. Component Position Within Chain Poker Genesis

The engine operates as part of the protocol architecture.

A simplified system relationship is:

```text
CHAIN POKER GENESIS
│
├── Protocol
│
├── Table System
│   ├── Table Identity
│   ├── Table State
│   ├── Table Manifest
│   └── Cryptographic Verification
│
├── Lobby
│   └── Table Selection
│
├── Seating Flow
│   └── Viewer Selection / Creation
│
├── Poker Table Viewer Creation Engine
│   ├── Template Engine
│   ├── Format Specification
│   ├── Viewer Generator
│   ├── Viewer Registry
│   └── Viewer Binding
│
└── Renderer
    └── Visual Table Representation
```

The engine is therefore a protocol-facing component while retaining an architectural separation from the table instance.

***

# 5. Two Viewer Access Paths

The protocol provides two principal ways to obtain a table viewer.

## 5.1 Viewer Creation Path

A participant may enter the viewer creation system independently of a particular table.

The participant may:

1. open the viewer creation engine;
2. select a predefined viewer template;
3. select a custom viewer configuration;
4. configure a default viewer;
5. provide visual assets;
6. provide optional code;
7. generate the viewer;
8. store or register the resulting viewer definition.

The resulting viewer does not have to be permanently bound to one specific table.

***

## 5.2 Table Seating Path

The second path occurs from the poker table lobby.

The participant selects a table and chooses:

> **Sit at Table**

The protocol then provides the option to:

```text
SIT AT TABLE
│
├── Use Existing Viewer
│
└── Create New Viewer
```

### Existing Viewer

The participant selects a previously created viewer.

The protocol obtains the selected table's identity and establishes the binding between:

```text
Viewer Definition
        +
Table Identifier
        +
Cryptographic Signature
```

The viewer then renders the selected table.

### Create New Viewer

The participant is sent to the Poker Table Viewer Creation Engine.

The participant creates or configures a new viewer.

After generation, the viewer is associated with the table selected in the seating flow.

This provides an integrated relationship between table access and viewer creation without embedding the table directly into the viewer definition.

***

# 6. Viewer Creation Modes

The engine provides two principal creation modes.

## 6.1 Pre-Designed Template

The participant may select a predefined viewer supplied by the Chain Poker Genesis ecosystem.

Example:

```text
VIEWER TEMPLATE MENU

[ Default Poker Table ]
[ Classic Table ]
[ Minimal Table ]
[ Tournament Table ]
[ Custom Template ]
```

Pre-designed templates define a known visual structure and implementation format.

***

## 6.2 Custom Template

The participant may create a custom viewer using the supported format specification.

The custom viewer may define:

- table dimensions;
- player positions;
- card positions;
- chip positions;
- pot presentation;
- betting areas;
- dealer position;
- action indicators;
- player information;
- table information;
- visual assets;
- typography;
- backgrounds;
- graphical elements;
- interactive elements;
- state indicators;
- animations where supported;
- other protocol-compatible presentation elements.

A custom viewer must remain compatible with the protocol's viewer format specification.

***

# 7. Default Viewer Creation

The protocol provides a dedicated operation for establishing a default viewer.

When the participant selects:

> **Set Default Table Viewer**

the engine may request the creation or configuration of the default viewer.

The configuration interface provides:

```text
DEFAULT TABLE VIEWER

Choose Default Image
Insert Custom Image
Insert Code

[ GENERATE ]
```

***

# 8. Default Image

The participant may select an image supplied by the system or viewer template.

The image acts as the visual foundation of the generated viewer.

The image itself does not establish table identity.

It is a presentation resource only.

***

# 9. Custom Image

The participant may insert a custom image.

The custom image may represent, for example:

- a table background;
- branding;
- decorative visual elements;
- thematic design;
- custom interface composition.

The engine validates the image according to the supported viewer format requirements.

The custom image remains a visual resource and does not contain authoritative table state.

***

# 10. Code-Based Viewer Generation

The engine may provide a code input mechanism for generating a viewer.

The participant may provide protocol-compatible viewer code.

The engine processes that code according to the viewer format specification and produces a viewer definition.

A code-generated viewer must comply with the protocol's compatibility, validation, and security requirements.

Code used to define presentation must not be treated as an independent authority over:

- table ownership;
- balances;
- ledger state;
- player identity;
- settlement;
- consensus;
- cryptographic truth.

***

# 11. Generate Operation

The **Generate** operation transforms the selected viewer configuration into a formal viewer definition.

Conceptually:

```text
TEMPLATE
   +
FORMAT
   +
ASSETS
   +
OPTIONAL CODE
   ↓
VIEWER GENERATOR
   ↓
VALIDATION
   ↓
CANONICAL VIEWER DEFINITION
```

The generated result may then be stored, identified, referenced, and used by the protocol.

***

# 12. Viewer Definition

A viewer definition describes the visual behavior and structure of the viewer.

A conceptual viewer definition may contain:

```text
Viewer Identifier
Viewer Version
Format Specification
Template Reference
Asset References
Layout Definition
Component Definitions
Rendering Rules
Interaction Definitions
Compatibility Requirements
Validation Metadata
Manifest Reference
```

The viewer definition must not require a permanently embedded poker table identity.

***

# 13. Separation From Table Identity

The architecture explicitly prohibits making the viewer itself the authoritative table identity.

The following relationship is therefore not required:

```text
Viewer
   ↓
Embedded Table
```

Instead, the runtime relationship is:

```text
Viewer
   +
Table Identifier
   +
Cryptographic Signature
   ↓
Verified Table Binding
```

This distinction is fundamental to the architecture.

***

# 14. Runtime Table Binding

When a viewer starts and does not yet have an active table binding, it requests the information necessary to select the table.

The viewer may request:

```text
TABLE IDENTIFIER
CRYPTOGRAPHIC SIGNATURE
```

The protocol then attempts to resolve and verify the referenced table.

Conceptually:

```text
USER
 │
 ▼
VIEWER
 │
 ├── Table Identifier
 └── Cryptographic Signature
       │
       ▼
TABLE RESOLUTION
       │
       ▼
SIGNATURE VERIFICATION
       │
       ▼
VALID TABLE
       │
       ▼
TABLE STATE
       │
       ▼
VIEWER RENDERING
```

***

# 15. Cryptographic Verification

The cryptographic signature exists to provide a verification mechanism for the table binding.

The viewer must not assume that an arbitrary identifier is sufficient to establish an authoritative table relationship.

The binding process should therefore conceptually verify:

```text
Table Identifier
      +
Cryptographic Signature
      ↓
Verification
      ↓
Accepted / Rejected
```

Only after successful validation should the viewer establish the active table relationship.

The exact cryptographic mechanism is defined by the corresponding Chain Poker Genesis protocol specifications.

***

# 16. Viewer-to-Table Relationship

The system allows:

### One Viewer → Multiple Tables

```text
             ┌── Table A
Viewer X ────┼── Table B
             └── Table C
```

provided that those tables satisfy the viewer's compatibility requirements.

### One Table → Multiple Viewers

```text
               ┌── Viewer A
Table X ───────┼── Viewer B
               └── Viewer C
```

This allows presentation to remain independent from the underlying table protocol state.

***

# 17. Table Lobby Integration

The lobby represents the primary discovery interface for available poker tables.

The seating operation creates the connection between table selection and viewer selection.

Conceptually:

```text
TABLE LOBBY
    │
    ▼
SELECT TABLE
    │
    ▼
SIT AT TABLE
    │
    ├── Use Existing Viewer
    │        │
    │        ▼
    │    Select Viewer
    │
    └── Create New Viewer
             │
             ▼
       Viewer Creation Engine
             │
             ▼
       Generate Viewer
```

After the viewer is selected or generated:

```text
Viewer
   +
Selected Table
   ↓
Cryptographic Binding
   ↓
Active Table Session
```

***

# 18. Existing Viewer Selection

When the participant chooses **Use Existing Viewer**, the system should expose viewers available to that participant or otherwise authorized by the protocol.

The selection may be based on:

- viewer identifier;
- compatibility;
- viewer version;
- supported table format;
- player configuration;
- stored viewer definitions.

The selected viewer then becomes the presentation layer for the table chosen in the lobby.

***

# 19. New Viewer Creation From Lobby

When the participant chooses **Create New Viewer**, the protocol preserves the selected table context while opening the viewer creation engine.

Conceptually:

```text
Selected Table
     │
     │ retained as seating context
     ▼
Create New Viewer
     │
     ▼
Viewer Creation Engine
     │
     ▼
Generate Viewer
     │
     ▼
Bind Generated Viewer
     │
     ▼
Enter Table
```

The table itself is not recreated by the viewer engine.

Only the presentation layer is being created.

***

# 20. Format Specification

The viewer engine depends on a formal viewer format specification.

The format specification defines the interoperable structure of a poker table viewer.

It may define:

```text
Canvas
Table Geometry
Seat Geometry
Card Geometry
Chip Geometry
Pot Geometry
Bet Geometry
Player Information
Action Information
Dealer/Button Position
Community Cards
Status Information
Table Metadata
Graphical Assets
Interaction Areas
Rendering Rules
State Mapping
Compatibility Rules
```

The specification establishes the boundary between protocol state and visual representation.

***

# 21. Protocol State vs. Visual State

The architecture distinguishes between authoritative protocol data and its visual representation.

### Authoritative Layer

```text
Table Identity
Player Identity
Game State
Bet State
Pot State
Ledger References
Cryptographic Proof
Protocol State
```

### Presentation Layer

```text
Position
Color
Image
Typography
Layout
Cards as graphics
Chips as graphics
Animations
Visual indicators
```

The presentation layer reflects protocol state but does not replace it.

***

# 22. Deterministic Viewer Generation

Viewer generation should produce a deterministic definition from the same canonical inputs.

Conceptually:

```text
Canonical Inputs
      ↓
Normalization
      ↓
Canonicalization
      ↓
Viewer Manifest
      ↓
Viewer Generator
      ↓
Canonical Viewer
```

Equivalent inputs should produce equivalent viewer definitions.

This makes the viewer compatible with the broader manifest-oriented architecture of Chain Poker Genesis.

***

# 23. Viewer Manifest

A generated viewer may be represented by a manifest containing references to:

```text
Viewer Identifier
Version
Format
Template
Assets
Code
Dependencies
Compatibility
Rendering Configuration
Integrity Data
```

The manifest provides a machine-readable description of the viewer.

The viewer manifest must remain distinguishable from the table manifest.

***

# 24. Table Manifest vs. Viewer Manifest

The architecture therefore contains two distinct conceptual objects.

### Table Manifest

Describes the protocol table.

```text
Table Identifier
Protocol Configuration
Participants
State
Cryptographic Data
Table Resources
```

### Viewer Manifest

Describes the table's visual interface.

```text
Viewer Identifier
Viewer Format
Template
Assets
Layout
Rendering Rules
Compatibility
```

Their relationship is:

```text
TABLE MANIFEST
      │
      │ binding
      ▼
VIEWER
      │
      ▼
VIEWER MANIFEST
```

Neither manifest replaces the other.

***

# 25. Lifecycle of a Viewer

The viewer lifecycle is:

```text
CREATE
   ↓
CONFIGURE
   ↓
VALIDATE
   ↓
CANONICALIZE
   ↓
GENERATE
   ↓
REGISTER / STORE
   ↓
SELECT
   ↓
BIND TO TABLE
   ↓
RENDER
   ↓
UNBIND / REUSE
```

A viewer can subsequently be reused with another compatible table.

***

# 26. Viewer Reusability

A viewer is reusable by design.

The system should not require the participant to create a new viewer for every table.

The participant may therefore maintain a collection of viewer definitions:

```text
MY VIEWERS

Viewer A
Viewer B
Viewer C
Viewer D
```

When entering another table, one of these viewers may be selected.

***

# 27. Viewer Compatibility

A viewer may impose compatibility requirements.

Examples include:

- supported table geometry;
- number of seats;
- supported poker variant;
- supported state fields;
- required protocol version;
- required rendering features.

Before binding, the protocol may verify:

```text
Viewer Compatibility
       +
Table Compatibility
       ↓
Binding Allowed / Rejected
```

***

# 28. Security Boundary

The viewer engine must not be permitted to alter authoritative protocol state merely through its presentation mechanisms.

Visual code or assets must therefore remain isolated from authoritative components unless explicitly exposed through approved protocol interfaces.

The conceptual security boundary is:

```text
┌──────────────────────────────┐
│      AUTHORITATIVE LAYER     │
│                              │
│ Table / Protocol / Ledger    │
│ Identity / Cryptography      │
└──────────────┬───────────────┘
               │
        Approved Interface
               │
┌──────────────▼───────────────┐
│       VIEWER LAYER           │
│                              │
│ Template / Assets / Renderer │
│ Presentation / Interaction   │
└──────────────────────────────┘
```

***

# 29. Conceptual User Flow

A complete user flow may be represented as follows:

```text
OPEN CHAIN POKER GENESIS
          │
          ▼
      TABLE LOBBY
          │
          ▼
      SELECT TABLE
          │
          ▼
     SIT AT TABLE
          │
    ┌─────┴─────┐
    ▼           ▼
USE EXISTING   CREATE NEW
   VIEWER        VIEWER
    │              │
    │              ▼
    │      VIEWER CREATION ENGINE
    │              │
    │       ┌──────┼───────┐
    │       ▼      ▼       ▼
    │   Template Image   Code
    │       │      │       │
    │       └──────┼───────┘
    │              ▼
    │           GENERATE
    │              │
    └───────┬──────┘
            ▼
     SELECT / GENERATE
          VIEWER
            │
            ▼
     TABLE IDENTIFIER
            +
     CRYPTOGRAPHIC SIGNATURE
            │
            ▼
       VERIFY TABLE
            │
            ▼
       BIND VIEWER
            │
            ▼
       RENDER TABLE
            │
            ▼
         PLAY / USE
```

***

# 30. Architectural Invariants

The following invariants define the architecture.

### Invariant 1

A viewer is not a poker table.

### Invariant 2

A viewer does not own authoritative table state.

### Invariant 3

A table does not depend on one permanent visual representation.

### Invariant 4

A viewer may be reused for multiple compatible tables.

### Invariant 5

A table may be represented by multiple compatible viewers.

### Invariant 6

Table binding requires a valid table identity and cryptographic verification according to the protocol.

### Invariant 7

The viewer format defines presentation capabilities, not ownership of protocol state.

### Invariant 8

The viewer generation process must produce a canonical representation from canonical inputs.

### Invariant 9

Creating a viewer and sitting at a table are separate operations that can be connected by the protocol.

### Invariant 10

The lobby provides a second entry path into the viewer system through the **Sit at Table → Existing Viewer / New Viewer** flow.

***

# 31. Formal Component Definition

The Poker Table Viewer Creation Engine can therefore be formally defined as:

> **A protocol component of Chain Poker Genesis by LAEV that transforms predefined or user-defined visual specifications into canonical poker table viewer definitions and provides the mechanisms required to select, validate, and cryptographically bind those viewers to independently identified poker table instances.**

***

# 32. Architectural Objective

The objective is to establish a presentation architecture in which:

```text
TABLE ≠ VIEWER
```

while maintaining a protocol-defined relationship:

```text
TABLE ↔ VERIFIED VIEWER BINDING
```

This allows Chain Poker Genesis to support a modular ecosystem in which table visualization can evolve independently from the underlying poker protocol.

The architecture consequently supports:

- reusable viewers;
- multiple visual interfaces;
- custom table presentation;
- predefined templates;
- user-created viewers;
- runtime viewer selection;
- cryptographically verified table binding;
- protocol/viewer separation;
- deterministic viewer generation;
- manifest-based representation.

***

# 33. Final Architectural Model

The complete conceptual model is:

```text
                         CHAIN POKER GENESIS
                                  │
               ┌──────────────────┴──────────────────┐
               │                                     │
          TABLE PROTOCOL                         VIEWER SYSTEM
               │                                     │
       ┌───────┴────────┐                 ┌──────────┴──────────┐
       │                │                 │                     │
 Table Identity     Table State      Creation Engine       Viewer Registry
       │                                    │
       │                          ┌─────────┴─────────┐
       │                          │                   │
       │                    Predefined           Custom
       │                    Templates           Templates
       │                          │                   │
       │                          └─────────┬─────────┘
       │                                    │
       │                                 Generate
       │                                    │
       │                             Viewer Definition
       │                                    │
       └───────────────┐                    │
                       │                    │
                       ▼                    ▼
                Cryptographic      Viewer Selection
                  Verification             │
                       │                    │
                       └─────────┬──────────┘
                                 ▼
                         VERIFIED BINDING
                                 │
                                 ▼
                            RENDERER
                                 │
                                 ▼
                           VISUAL TABLE
```

The defining architectural principle is therefore:

> **The viewer is created independently, selected or generated as part of the seating process, and cryptographically bound at runtime to the table identified by the protocol.**

***

# 34. Status

This document defines the **formal architecture and functional behavior** of the Poker Table Viewer Creation Engine.

It constitutes the architectural reference for subsequent:

- implementation;
- repository organization;
- viewer format specification;
- manifest definition;
- data structures;
- validation rules;
- protocol interfaces;
- rendering implementation;
- table-lobby integration;
- testing;
- reference implementations.

This document does not, by itself, constitute implementation of the engine. It defines the required architecture against which implementation can be audited.
