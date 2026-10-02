# Installation Engine — Security Model

**Version:** 1.0 historical security boundary

## Security Objective

The Installation Engine establishes the first trust and integrity layer before a Genesis Player Node is permitted to begin complete protocol operation.

## Historical Security Checks

The source specification requires validation of:

- code integrity;
- official file hashes;
- engine compatibility;
- remote-node integrity;
- signs of alteration;
- signs of manipulation;
- signs of corruption;
- signs of attack.

## Trust Boundary

The historical architecture contains two initial trust domains:

1. the local Genesis Player Node;
2. remote cloud virtual backup infrastructure.

The Installation Engine coordinates validation between them.

## What the Historical Specification Does Not Yet Define

The PDF does not establish the cryptographic trust architecture required to implement these checks securely.

The following must therefore remain open engineering work:

- cryptographic hash algorithm;
- digital signature algorithm;
- root public key;
- trust-anchor provisioning;
- signed manifests;
- certificate or key hierarchy;
- revocation;
- anti-rollback protection;
- secure update authorization;
- remote-node authentication;
- quorum or multi-node validation;
- compromised-node response;
- offline recovery;
- audit-log format.

## Security Principle

No undocumented mechanism should be presented as part of v1.0.

The repository reconstruction must distinguish:

**historically specified**  
from  
**technically proposed**  
from  
**implemented**.

This distinction is required to preserve the historical record and prevent undocumented assumptions from becoming protocol rules.
