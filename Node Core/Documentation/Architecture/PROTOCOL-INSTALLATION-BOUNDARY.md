# Protocol Installation Boundary

**Project:** Chain Poker Genesis by LAEV  
**Component:** Node Core → Chain Poker Genesis

## Purpose

This boundary separates the protocol-neutral Node Core from the later Chain Poker Genesis installation layer.

## Node Core Side

The Node Core completion state MUST preserve:

    protocol_associations = []
    cpg_protocol = NOT_INSTALLED
    synchronization = NOT_EVALUATED

## Boundary State

The boundary guard reports `ARMED` when Node Core is complete and CPG remains uninstalled.

`ARMED` does not mean CPG is installed. It means the repository has a verified separation point at which a future protocol installation component may be introduced.

## Prohibited Crossings

Node Core bootstrap, verification, runtime, health, recovery, and release-integrity operations MUST NOT install, activate, associate, or synchronize Chain Poker Genesis.
