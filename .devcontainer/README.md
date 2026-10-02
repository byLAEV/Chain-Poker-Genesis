# .devcontainer

## Purpose

This directory defines the development-container configuration used to provide a reproducible development environment for **Chain Poker Genesis**.

It is development infrastructure, not part of Node Core or the CPG Protocol.

## Scope

It may contain `devcontainer.json`, container definitions, development dependencies, development tooling, environment initialization and editor integration.

## GitHub Codespaces

The configuration may be used by GitHub Codespaces to provide a consistent development environment for building, inspecting and testing the repository.

The environment should not embed runtime state or protocol state into the development container.

## Reproducibility

Development dependencies should be explicitly declared where practical. The objective is reproducible development across supported environments while keeping development tooling separate from protocol execution.

## Security

Development credentials, private keys, wallet secrets and production secrets must never be committed to this directory. Environment-specific secrets should use appropriate secret-management mechanisms.

## Development Rule

Changes to the development environment should improve reproducibility and workflow without changing the architectural definition of Node Core or CPG Protocol.

## Status

**Canonical development-environment directory — configuration in progress.**
