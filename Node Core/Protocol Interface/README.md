# Node Core Protocol Interface

**Status:** IMPLEMENTED
**Version:** 1.1.0

Protocol Interface is the boundary between the protocol-neutral Node Core and independently installed protocol engines.

Implemented:
- protocol discovery records;
- manifest validation;
- capability compatibility checks;
- protocol registration;
- independent protocol installation state;
- protocol activation, suspension and removal;
- protocol descriptors and lifecycle records.

Node Core does not implement protocol consensus, ledger rules, player state, table state, settlement or application-specific semantics.

Protocol engines are independently versioned and are not represented as global Node Core versions.
