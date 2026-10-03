# Node Core Implementation Workflow

## Development loop

1. Select one Node Core phase from the master plan.
2. Read the governing specification and contract.
3. Inspect current implementation and dependencies.
4. Implement the smallest coherent change.
5. Add or update deterministic tests.
6. Run the repository Node Core audit and applicable tests through GitHub Actions.
7. Inspect failures and correct the implementation.
8. Record verification evidence.
9. Advance only after the phase gate passes.

## GitHub workflow

`Pull Request / Push → Audit → Manifest/Schema Validation → Compile → Unit Tests → Integration Tests → Verification`

Changes affecting Node Core should be covered by the Node Core workflow.

## Codespaces workflow

Codespaces provides a reproducible development environment. Its setup must be able to execute the same audit and test commands used by CI.

## Local handoff workflow

GitHub verification is a precondition, not a substitute for local execution. The final handoff requires a clean-environment installation test and operational verification.

## Change discipline

- Keep Node Core and CPG Protocol boundaries explicit.
- Do not silently change specifications while implementing.
- Do not mark a phase complete without evidence.
- Prefer deterministic tests and reproducible commands.
- Keep implementation changes traceable to a documented requirement.
