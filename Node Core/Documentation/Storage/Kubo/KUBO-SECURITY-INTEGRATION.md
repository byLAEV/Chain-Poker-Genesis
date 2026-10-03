# Kubo Security Integration

## Security boundary

Kubo's administrative RPC must not be exposed as an unprotected network service.

Node Core should prefer a localhost/socket boundary and explicit authorization for any broader access.

## Secrets

Node Core must not copy private Node Core keys into Kubo merely to make storage work.

Provider credentials and Node Core cryptographic identity remain separate unless a future formal specification explicitly defines a secure interoperability mechanism.

## Content

IPFS content addressing identifies bytes; it does not by itself provide application-level confidentiality.

Restricted Node Core objects therefore require Node Core encryption before publication to Kubo.

## Gateway

The Gateway is a retrieval interface. It must not be treated as an administrative control interface.

## Failure handling

Security failures are not ordinary provider outages.

The adapter must distinguish:

- unavailable;
- timeout;
- unauthorized;
- invalid response;
- integrity failure;
- incompatible version;
- malformed CID;
- policy violation.

## Upgrade

Kubo version changes must pass Node Core compatibility tests before production activation.
