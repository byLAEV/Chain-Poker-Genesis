# Kubo Release Source and Platform Matrix v1.0

**Status:** CANONICAL DESIGN

## Release source

Node Core uses the official Kubo release distribution as the installation source.

The resolver MUST obtain release metadata before selecting a package. The selected record must preserve:
- Kubo version;
- OS;
- architecture;
- distribution filename;
- official source;
- expected integrity evidence;
- resolution timestamp.

The installer MUST NOT scrape arbitrary mirrors or accept a user-supplied package as an official release without an explicit offline/provisioned-install mode contract.

## Linux — reference implementation

Supported architecture targets for the first implementation:
- amd64 / x86_64;
- arm64 / aarch64.

Linux is the first complete implementation target.

## Windows — planned implementation

Logical targets:
- amd64 / x86_64;
- arm64 / ARM64 where an official compatible Kubo distribution is available.

The logical provider contract remains identical, but executable invocation, process management, permissions and path normalization are platform-specific.

## iOS — deferred platform

The Linux model assumes a managed long-running Kubo process and direct filesystem/process lifecycle control. iOS requires a separate feasibility and platform contract.

iOS = DEFERRED / SEPARATE PLATFORM CONTRACT REQUIRED.

## Release policy

Default: LATEST_COMPATIBLE_STABLE

Alternative: EXACT_VERSION

The resolved release is pinned after selection. A newer release is never substituted during the same installation transaction.

## Maintenance policy

Release selection must evaluate compatibility and maintenance metadata, not version number alone.

A release may be rejected if:
- no official artifact exists for the host;
- integrity metadata is unavailable;
- the release is prerelease under the stable policy;
- the release is outside Node Core compatibility policy;
- maintenance/security policy marks it unacceptable.

The current upstream release observed during design review is evidence only; Node Core MUST NOT hard-code that version into the installer.
