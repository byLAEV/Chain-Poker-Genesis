# External Identity Implementation References

This implementation uses external open-source projects as architectural references, not as CPG identity rules.

## libp2p
The libp2p identity model demonstrates a useful pattern: a cryptographic public key is the root of peer identity, the peer identifier is deterministically derived from encoded public-key material, and received public keys are checked against the expected peer identifier. See the libp2p peer-ID specification and identify service.

- Reference: libp2p Peer IDs and Keys.
- Reference: go-libp2p Identify service.

Node Core adopts the *pattern* of deterministic key-to-identifier binding, but keeps LAEV's canonical SHA-256 identity profile and Node Life model.

## Matrix/Synapse
Synapse demonstrates operational patterns for signing-key lifecycle, key refresh, trusted-key configuration and separation of public verification material from private signing material.

Node Core adopts only the architectural pattern. It does not import Matrix identity semantics.

## License/provenance rule
No third-party source code is copied into Node Core unless its license and compatibility are explicitly verified. The current implementation is independently written from the repository's own specification while using public project patterns as design references.
