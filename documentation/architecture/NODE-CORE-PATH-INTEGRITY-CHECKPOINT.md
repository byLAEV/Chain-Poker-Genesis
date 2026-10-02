# Node Core Path Integrity Checkpoint

**Scope:** Structural migration safety before executable Node Core relocation.

## Checked surfaces

- GitHub Actions Node Installation Validation workflow
- release integrity artifact list
- installation-manifest schema validation path
- specification coverage audit path
- canonical Node Core documentation paths

## Result

### Documentation path

Canonical Node Core specifications are now referenced under:

`documentation/node-core/`

### CI path trigger

The Node Installation Validation workflow has been updated to trigger on:

`documentation/node-core/**`

The executable implementation path remains unchanged:

`reference-implementation/node-installation/**`

### Release integrity

The release integrity artifact list already references the canonical documentation paths. It continues to reference the existing executable implementation paths.

This is intentional: documentation migration and executable migration remain separate operations.

## Gate status

```
DOCUMENTATION PATHS     PASS
CI DOCUMENTATION PATH   PASS
RELEASE ARTIFACT MAP    PASS
EXECUTABLE PATH         PROTECTED
EXECUTABLE MOVE         BLOCKED
```

## Next gate

The next operation is not yet a physical move.

The remaining requirement is to establish a **behavioral baseline run** from the current reference implementation and capture its expected outputs before changing its path.

After that baseline is recorded, the implementation can be relocated as one isolated structural change and validated against the captured baseline.


## Clean Validation Trigger

This marker triggers a fresh Node Core baseline validation after the documented path repairs. It does not modify Node Core runtime behavior.


## Classification correction

The release-integrity artifact list was corrected to keep Node Core audit/completion evidence under `docs/node/` until those artifacts receive their own canonical migration decision. This prevents the release verifier from asserting paths that do not yet exist.
