# USB Hardware Signer Specification v1.0

## 1. Scope

Defines the protocol-neutral Node Core interface for requesting cryptographic approval from an external HD hardware wallet over USB.

## 2. Required operations

The adapter SHALL expose:

- `enumerateDevices`
- `getDeviceInfo`
- `getPublicKey`
- `getExtendedPublicKey`
- `requestApproval`
- `signApproval`
- `disconnect`

## 3. Approval request

An approval request SHALL contain:

- request identifier;
- operation type;
- canonical payload digest;
- protocol/context identifier;
- requested derivation path or signer reference;
- human-readable confirmation metadata when supported by the device;
- expiration or anti-replay value.

The device should display enough information for the user to understand what is being approved. The exact display capability is device-dependent.

## 4. Signature result

A signer result SHALL contain:

- request identifier;
- device identifier;
- public-key or signer reference;
- signature algorithm;
- signature;
- payload digest;
- derivation-path reference when applicable;
- verification status.

## 5. Anti-replay rule

Node Core MUST bind a signature to the exact canonical payload digest and approval request context. A signature for one request MUST NOT silently satisfy another request.

## 6. Private-key rule

The adapter MUST never request or accept raw private-key material from the hardware wallet.

## 7. HWI integration boundary

`bitcoin-core/HWI` is the reference transport/device interface. It provides a standard way for software to interact with hardware wallets without implementing device-specific drivers in the caller.

Node Core SHOULD integrate HWI through a controlled provider/bridge rather than copying device-specific implementations into protocol code.

## 8. CPG separation

This component does not contain:

- table consensus;
- table wallet state;
- settlement logic;
- rake logic;
- poker rules;
- CPG ledger semantics.

Those components submit approval requests to this signer boundary when an external signature is required.
