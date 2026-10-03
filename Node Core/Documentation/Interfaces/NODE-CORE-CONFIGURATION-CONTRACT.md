# Node Core Configuration Contract
Status: NORMATIVE DESIGN BASELINE

Configuration must be:
- canonical;
- schema-validated;
- versioned;
- integrity-checked;
- explicit about defaults;
- separated from protocol configuration.

Required domains:
identity, storage, network, runtime, security, recovery, engines, protocol interface.

Invalid or ambiguous configuration fails closed.
