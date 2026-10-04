# Kubo Managed Provider Foundation

Linux reference implementation foundation for the Kubo Node Installer / Manager.

Current implementation scope:
- release resolution from supplied official metadata;
- Linux/Windows platform vocabulary with Linux implementation first;
- canonical Node Core path derivation;
- explicit absolute IPFS_PATH;
- atomic provider-state persistence.

Not yet implemented:
- remote release metadata retrieval;
- package download;
- package checksum verification against a live release;
- extraction/install;
- Kubo repository initialization;
- process lifecycle;
- health checks;
- initial synchronization;
- Dual Storage activation.

These boundaries are intentional.