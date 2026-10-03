# Cryptography Providers

**Status:** IMPLEMENTED

External cryptographic systems are exposed through explicit Node Core provider adapters.

Implemented provider boundaries:
- Coincurve / libsecp256k1
- GPGME / GnuPG
- PyNaCl / libsodium
- Bitcoin Core HWI / hardware wallets

Each adapter is pinned to a verified upstream repository commit and fails explicitly when its runtime dependency is unavailable.

The upstream projects remain external dependencies; Node Core does not copy or claim ownership of their implementations.
