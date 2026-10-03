# Recovery API

Provides controlled recovery operations for Node Core state and storage.

## Contract

- inspectRecoveryState
- validateRecoverySource
- prepareRecovery
- executeRecovery
- verifyRecovery
- resumeNode

Recovery must preserve identity and must not silently activate application protocols.
