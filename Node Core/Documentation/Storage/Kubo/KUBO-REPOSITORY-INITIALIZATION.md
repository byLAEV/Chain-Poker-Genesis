# Kubo Repository Initialization

Repository initialization is a distinct lifecycle stage after Kubo package installation.

The initializer invokes the installed Kubo executable with an explicit absolute `IPFS_PATH`.

It verifies:
- repository config exists;
- config is valid JSON;
- Kubo generated a PeerID;
- the repository version marker exists.

The Kubo PeerID is Kubo repository identity. It is not the Node Core cryptographic identity and does not replace it.

The initializer does not start the Kubo daemon and does not enable Dual Storage.