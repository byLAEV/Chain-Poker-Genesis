# Consensus Engine

Coordinates the Node Core Consensus process.

Responsibilities:

- collect participant state;
- invoke eligibility validation;
- invoke Proof of Function verification;
- process preferences;
- apply consensus rules;
- resolve conflicts;
- produce accepted state;
- emit evidence.

The engine remains independent of CPG semantics.
