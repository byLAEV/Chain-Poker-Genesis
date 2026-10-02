# Graphical Interface Engine — Functional Specification

**Version:** 1.0  
**Status:** Historical functional reconstruction  
**Source:** 2.0 Graphical Interface Engine — Chain Poker Genesis by LAEV

## 1. Functional Definition

The Graphical Interface Engine manages the main graphical interface of an installed Chain Poker Genesis node.

It provides the user-facing access layer for protocol modules, tools, configuration, node administration, ledger exploration, and installed functions.

## 2. Functional Exclusion

This engine does not define or execute:

- poker rules;
- poker-table game logic;
- internal poker-table operation.

## 3. Principal Access Functions

Version 1.0 defines seven principal access functions:

1. Available Tables.
2. Create Table.
3. Connect Through Cryptographic Signature.
4. Ledger Explorer.
5. Configuration.
6. Node Administration.
7. Tools.

## 4. Internal Access

The interface provides access to internal menus and submodules covering:

- system configuration;
- logs;
- network administration;
- node administration;
- protocol tools;
- additional installed functions.

## 5. Node Information

The interface displays general operational information including:

- node status;
- node operating time;
- installed-system information.

## 6. Evolution

The engine is independently versionable for graphical and interaction improvements.

Changes may concern the visual layer and navigation without redefining the underlying poker rules or table logic.

## 7. Update Acceptance

The historical specification requires updates to be accepted through the player-node consensus system.

The Consensus Engine is the designated source for the detailed governance rules.

## 8. Undefined Technical Requirements

The historical source does not define exact:

- APIs;
- data schemas;
- UI framework;
- rendering technology;
- state machine;
- update package format;
- cryptographic update mechanism;
- consensus thresholds;
- rollback procedure.

Those requirements remain pending dedicated technical specifications.
