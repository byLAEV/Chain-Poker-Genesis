# Node Core External Adapter Inventory

This directory records external API/adaptor sources required by Node Core.

## Integration rule

External projects are not copied wholesale. Node Core vendors only an adapter, contract, or explicitly licensed source component when needed. Each integration records upstream repository, license, pinned revision, local purpose, and modifications.

## Current providers

| Provider | Upstream | Node Core use | Local policy |
|---|---|---|---|
| Kubo | https://github.com/ipfs/kubo | IPFS/Kubo storage provider | Adapter only; no Kubo internals |
| libp2p | https://github.com/libp2p | P2P transport/network provider | Adapter/contract only |
| GPGME | https://github.com/gpg/gpgme | GnuPG crypto provider | Adapter only |
| OpenPGP.js | https://github.com/openpgpjs/openpgpjs | OpenPGP crypto provider | Adapter only |

## Not vendored yet

No upstream source should be copied into Node Core until its exact license, revision and required files have been verified.

This prevents accidentally importing an entire external implementation, stale code, incompatible licenses, or undocumented dependencies.

## Required next implementation step

For each provider:

1. pin an upstream release/commit;
2. inspect its license;
3. identify exact API surface used;
4. create a minimal local adapter;
5. preserve upstream attribution/license notices;
6. document modifications;
7. add compatibility tests;
8. keep provider implementation outside Node Core semantics.
