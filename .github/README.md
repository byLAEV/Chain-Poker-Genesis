# .github

## Purpose

This directory contains repository-level GitHub configuration and automation for **Chain Poker Genesis**. It is not part of Node Core or the CPG Protocol runtime.

## Scope

It may contain GitHub Actions workflows, issue and pull-request templates, repository automation, contribution configuration, code ownership configuration, CI/CD definitions, and validation or repository-integrity checks.

## Architectural Boundary

```text
Chain-Poker-Genesis
├── Node Core/          runtime node infrastructure
├── CPG Protocol/       CPG protocol implementation
├── .github/            repository automation
└── .devcontainer/      development environment
```

GitHub configuration may validate, test, build or document the project, but it does not become part of the runtime architecture.

## Repository Integrity

Automation should support deterministic validation, manifest consistency, structural checks, tests, implementation verification and documentation integrity. It must not silently redefine protocol behavior.

## Development Rule

Repository automation must reflect the canonical architecture rather than obsolete historical layouts.

## Status

**Canonical repository infrastructure directory — configuration in progress.**
