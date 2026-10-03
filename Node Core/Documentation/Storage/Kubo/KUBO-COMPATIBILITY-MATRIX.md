# Kubo Compatibility Matrix

| Dimension | Requirement |
|---|---|
| Kubo version | Record exact version |
| API/RPC | Record supported API surface |
| Repository format | Provider-owned and version-checked |
| CID formats | Explicitly tested |
| UnixFS | Explicitly tested when used |
| Pinning | Explicitly tested when used |
| Gateway | Explicitly tested when used |
| Routing | Explicitly tested when used |
| Encryption | Node Core responsibility before provider write |
| Local fallback | Must work independently |
| Restart | Must recover provider state |
| Upgrade | Must pass compatibility vectors |

## Status

The matrix is a specification artifact until a concrete Kubo version is pinned and integration tests are executed.
