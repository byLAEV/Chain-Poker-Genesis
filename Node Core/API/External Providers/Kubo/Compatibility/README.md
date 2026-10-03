# Kubo Compatibility

Baseline: v0.43.1

Upstream commit: 46a53f55dd670059c86b7315919cd2e01caa3113

Compatibility must verify:

- daemon/API reachability;
- add/get round trip;
- CID preservation;
- integrity verification;
- provider health;
- failure and local-storage fallback;
- authentication/endpoint protection.

A Kubo upgrade requires a new compatibility run and pinned revision.