# Cryptographic Connection Engine — Security Model

**Version:** 1.0 historical security boundary

## Security Objective

The engine must allow a Genesis Player Node to establish cryptographic identity without unnecessarily exposing private credentials.

## Historical Security Properties

The source document establishes that hardware-wallet private keys remain inside the hardware device, the operating system does not need to receive the hardware private key, hardware-generated signatures are returned as cryptographic results, users retain control over their identity-management method, and credential management is separated from unrelated protocol engines.

## Threat Boundary

The engine must be treated as a security boundary between the Player Node software environment, locally stored software credentials, external hardware-wallet devices, and the rest of Chain Poker Genesis.

## Sensitive Data

Potentially sensitive material includes private keys, BIP-39 seeds, seed phrases, temporary secret material, and credentials used to unlock local secret storage.

The historical specification does not authorize logging, transmission, or persistence of these values beyond what is necessary for the selected credential method.

## Hardware Wallet Principle

For hardware-backed identity, the implementation should preserve the historical requirement that the private key remain in the hardware device. Authentication should therefore use signatures or another formally defined cryptographic result rather than exporting the private key.

## Open Security Requirements

The historical document does not define the complete security implementation. Future technical specifications must establish cryptographic algorithms, secure random-number generation, key derivation, seed handling, encrypted secret storage, memory zeroization, anti-exfiltration controls, hardware-wallet authentication, replay protection, message domain separation, signature verification, error handling, recovery, revocation, and audit/privacy requirements.

## Security Rule

No algorithm, key format, derivation path, wallet protocol, or trust mechanism should be treated as an official Chain Poker Genesis rule solely because it is technically common or convenient. Until formally specified, those elements remain open technical decisions.
