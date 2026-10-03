# Identity API

Defines the Node Core identity service boundary.

## Contract

- getNodeIdentity
- validateIdentity
- getIdentityState
- getPublicIdentity
- createIdentityBinding
- verifyIdentityBinding
- getCredentialReference
- recoverIdentity

Private keys remain outside the API boundary where the credential model requires external custody.
