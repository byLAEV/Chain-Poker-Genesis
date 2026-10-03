# External Adapter Integration Record

The Node Core integration is intentionally adapter-based. No external repository is copied wholesale into Node Core.

## Kubo
Used by Storage Provider API for distributed/IPFS storage. Pinned at v0.43.1.

## libp2p
Used by Network API for P2P connectivity. Pinned reference is py-libp2p v0.6.0; the concrete runtime language/provider must be selected before implementation.

## GPGME
Optional provider for GnuPG-backed cryptographic operations. Pinned at gpgme-2.2.0.

## OpenPGP.js
Optional provider for OpenPGP operations. Pinned at v6.3.2.

## Important

These are provider references, not claims that every provider is already executable inside Node Core. The next implementation stage must add actual source adapters in the runtime language selected for Node Core, plus CI compatibility tests.

Licenses and upstream notices must be preserved when source is vendored. Binary/package dependencies remain external unless explicitly approved for vendoring.