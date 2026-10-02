# Installation Engine — Versioning Policy

## Installation Engine v1.0

The historical document identifies Installation Engine v1.0 as the official base installer.

Its documented responsibility is to deploy and verify the general structure while allowing individual engines to maintain their own evolution cycles.

## Engine-Level Versioning

The protocol architecture distinguishes between:

- engines with permanent or immutable versions;
- engines whose versions may evolve independently.

The historical example is the Texas Hold'em Poker Rules Engine v1.0, described as permanent.

Other engines may be versionable according to their function and security requirements.

## Compatibility Principle

An update to one engine should not implicitly modify unrelated engines.

Future technical specifications must define:

- version identifiers;
- compatibility ranges;
- dependency declarations;
- migration rules;
- rollback rules;
- update authorization;
- authenticity verification;
- distribution mechanisms.

## Historical Boundary

The v1.0 Installation Engine document does not define a complete update protocol. References to future authorized links, validation mechanisms, or player-node distribution describe architectural intentions rather than an implemented update mechanism.
