# Node Core Storage Contract
Status: NORMATIVE DESIGN BASELINE

## Required operations
- create
- read
- write
- update
- delete
- exists
- locate
- verify
- synchronize
- recover

## Required metadata
object_id, version, content_hash, storage_class, location, state, created_at, updated_at.

## Required separation
object_id ≠ operation_id ≠ content_hash ≠ CID.

## Providers
Local Storage is the authoritative fallback for node-local operation. Kubo/IPFS is an external distributed provider accessed only through its adapter/API boundary.

## Failure
A provider failure must produce an explicit state and must not silently destroy valid local state.

## Security
Path traversal, unauthorized access, protocol-reserved paths and integrity failures fail closed.
