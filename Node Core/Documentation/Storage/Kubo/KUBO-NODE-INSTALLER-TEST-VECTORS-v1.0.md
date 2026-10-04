# Kubo Node Installer / Manager Test Vectors v1.0

**Status:** CANONICAL DESIGN TEST SET

| ID | Scenario | Expected result |
|---|---|---|
| KUBO-INSTALL-0001 | Resolve latest compatible stable Linux amd64 release | Deterministic release record created |
| KUBO-INSTALL-0002 | Resolve latest compatible stable Linux arm64 release | Correct architecture artifact selected |
| KUBO-INSTALL-0003 | Exact version pin | Pinned release selected; no newer substitution |
| KUBO-INSTALL-0004 | Missing release metadata | Selection rejected |
| KUBO-INSTALL-0005 | Unsupported architecture | Selection rejected |
| KUBO-INSTALL-0006 | Integrity mismatch | Package rejected; provider not activated |
| KUBO-INSTALL-0007 | Executable version mismatch | Installation rejected |
| KUBO-INSTALL-0008 | Repository path outside Node Core root | Initialization rejected |
| KUBO-INSTALL-0009 | Relative IPFS_PATH | Provider rejected |
| KUBO-INSTALL-0010 | Existing operator home .ipfs | Managed instance ignores it and uses explicit IPFS_PATH |
| KUBO-INSTALL-0011 | Successful repository initialization | REPOSITORY_INITIALIZED |
| KUBO-INSTALL-0012 | Kubo process starts | HEALTHY after successful health check |
| KUBO-INSTALL-0013 | Kubo exits unexpectedly | State becomes DEGRADED/FAILED according to policy |
| KUBO-INSTALL-0014 | Initial sync interrupted | SYNC_FAILED with resumable synchronization state |
| KUBO-INSTALL-0015 | Initial sync completed | COHERENCE_VERIFICATION |
| KUBO-INSTALL-0016 | Coherence verification succeeds | READY |
| KUBO-INSTALL-0017 | Coherence verification fails | READY forbidden |
| KUBO-INSTALL-0018 | Dual Storage requested before READY | Request rejected |
| KUBO-INSTALL-0019 | Node Core restarted with stale PID | PID not treated as proof of running process |
| KUBO-INSTALL-0020 | Upgrade vA to vB | vB installed beside vA; vA not overwritten before explicit activation |
| KUBO-INSTALL-0021 | Removal | Kubo provider removed without deleting Node Core Local Storage |
| KUBO-INSTALL-0022 | iOS provisioning request | Deferred; platform-specific contract required |
