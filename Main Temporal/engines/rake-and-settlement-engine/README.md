# Rake Engine and Monetary Settlement Flow

**Chain Poker Genesis by LAEV (peroqtdigo)**

Official technical specification companion for document **5.0_Rake Engine and Monetary Settlement Flow_CPG.pdf**.

## Purpose

This engine defines the protocol workflow for:

1. determining an eligible poker pot;
2. calculating the configured rake;
3. recording the calculation in the Private Off-Chain Ledger;
4. moving the rake through the table operational wallet;
5. invoking the Monetary Settlement Engine;
6. allocating the rake between the Foundation and the external AkaMoto Rie L company wallet;
7. preserving a cryptographically auditable trail.

## Canonical source

The original PDF remains the historical source document:

[5.0_Rake Engine and Monetary Settlement Flow_CPG.pdf](../../5.0_Rake%20Engine%20and%20Monetary%20Settlement%20Flow_CPG.pdf)

This Markdown document structures the specification for repository navigation and implementation analysis. It does not silently replace the PDF.

## Default economic configuration

| Parameter | Value |
|---|---|
| Protocol version | 1.0 |
| Game | Texas Hold'em Cash Game |
| Rake | 3% |
| Foundation allocation | 11% of rake |
| AkaMoto Rie L allocation | 89% of rake |
| Settlement destination | One Bitcoin wallet controlled by AkaMoto Rie L |

The 11% + 89% allocation applies to **100% of the calculated rake**, not to the players' pot.

## Architectural position

`Poker Table → Hand Completion → Rake Engine → Private Off-Chain Ledger → Table Operational Wallet → Monetary Settlement Engine → Final Destinations`

The Rake Engine is therefore not the same component as the Monetary Settlement Engine. The former determines and records the obligation; the latter performs final monetary settlement.

## External company boundary

The specification defines AkaMoto Rie L as an entity external to Chain Poker Genesis. The protocol transfers the configured 89% allocation to its designated Bitcoin wallet; internal company accounting, liquidity, fiat conversion and business operations are outside the protocol boundary.

Statements in the source document concerning licensing, regulation or compliance should be treated as **requirements/claims of the specification**, not as independent proof that a particular jurisdictional authorization exists.

## Related components

- [Private Off-Chain Ledger Engine](../private-off-chain-ledger-engine/README.md)
- [Monetary Settlement Engine](../../12.0%20Monetary%20Settlement%20Engine__.pdf)
- [Table Wallet Engine](../../9.0%20Table%20Wallet%20Engine_-%20CHAIN%20POKER%20GENESIS%20BY%20LAEV%20(peroqtdigo).pdf)

## Implementation status

**Specification layer:** defined  
**Reference implementation:** not yet defined by this document  
**Production financial deployment:** not established by this document
