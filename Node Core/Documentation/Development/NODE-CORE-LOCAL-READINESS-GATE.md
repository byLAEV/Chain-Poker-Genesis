# Node Core Local Readiness Gate

## Objective

Determine whether the repository contains a reproducible Node Core implementation that is ready to be taken to a local machine for real execution.

## Required sequence

1. Clean environment.
2. Obtain the repository at the verified commit.
3. Install Node Core dependencies.
4. Initialize Node Core.
5. Establish or import cryptographic identity according to the installation contract.
6. Initialize storage.
7. Validate configuration and Node Core manifest.
8. Run installation verification.
9. Start Node Core.
10. Confirm readiness.
11. Stop Node Core cleanly.
12. Restart Node Core.
13. Verify persistent state and identity.
14. Exercise the defined recovery path.
15. Run final verification.

## Pass criteria

The gate passes only when:

- installation is reproducible;
- initialization succeeds;
- identity persists correctly;
- required storage behavior is operational;
- runtime reaches a valid readiness state;
- restart preserves required state;
- recovery procedures work;
- verification exits successfully;
- no unresolved critical implementation defect remains.

## Evidence

The final record must identify:

- source commit;
- environment;
- installation procedure;
- commands executed;
- test results;
- verification results;
- known limitations.

A successful GitHub Actions run alone does not constitute this final gate.
