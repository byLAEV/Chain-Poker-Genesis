# Node Core Schema Reconciliation

## Finding

The current schema set is not one homogeneous generation. It contains at least two manifest generations and different identifier conventions.

### Canonical candidates

| Schema | Role | Finding |
|---|---|---|
| `node-configuration.schema.json` | node configuration | Canonical Node Core candidate |
| `node-identity.schema.json` | identity metadata | Canonical Node Core candidate |
| `node-runtime-state.schema.json` | runtime state | Canonical Node Core candidate |
| `node-recovery.schema.json` | recovery metadata | Canonical Node Core candidate |
| `storage-manifest.schema.json` | runtime storage manifest | Canonical storage candidate |
| `storage-object.schema.json` | storage object | Canonical storage candidate |
| `storage-object-registry.schema.json` | object registry | Canonical storage candidate |
| `storage-provider.schema.json` | provider status | Canonical storage candidate |
| `node-installation-manifest.schema.json` | installation manifest | Legacy/installation-generation candidate; must be reconciled |
| `node-core-installation-manifest.schema.json` | completion/ready manifest | Newer completion-gate candidate; must be reconciled |
| `protocol-installation-boundary.schema.json` | protocol boundary | Boundary schema; not generic runtime storage |

## Critical issue

`node-installation-manifest.schema.json` and `node-core-installation-manifest.schema.json` describe overlapping installation concepts but are not identical.

The first includes an installation identity status and a broader readiness enum. The second requires a fully READY node and explicitly constrains protocol associations to zero and CPG Protocol to NOT_INSTALLED.

They must not both be declared canonical without an explicit version relationship.

## Identifier issue

Several schemas use `cpg://node-core/schema/...` identifiers while older schemas use GitHub URLs.

Before relocation, the repository should establish one canonical schema identifier policy. Moving files without resolving this would create ambiguous schema identity.

## Synchronization issue

The object registry already contains detailed synchronization states, while the installation manifest deliberately records synchronization as `NOT_EVALUATED`.

This is not necessarily contradictory: installation readiness and distributed synchronization are different lifecycle gates. The distinction should be documented and tested.

## Required action before schema migration

1. Declare the canonical installation-manifest generation.
2. Assign explicit versions to superseded schemas.
3. Establish one `$id` policy.
4. Update consumers and tests to reference the canonical generation.
5. Preserve superseded schemas as historical/versioned artifacts rather than silently deleting them.
6. Only then move schemas into the canonical Node Core documentation/schema boundary.

## Migration decision

**Do not physically move the schema files yet.**

The correct next operation is schema canonicalization, not folder movement.
