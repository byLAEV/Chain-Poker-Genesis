# GPGME Adapter

Purpose: provide a controlled provider boundary for GnuPG-backed cryptographic operations.

Pinned reference: GPGME gpgme-2.2.0 — 6b075516b88e3df70694a6f8cb9471388aa78aa8.

The adapter may expose encryption, decryption, signing, verification and key operations selected by the Node Core Cryptography API.

Private keys remain under the configured credential/custody boundary.