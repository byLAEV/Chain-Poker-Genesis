# Node Core API Catalog
Status: NORMATIVE DESIGN BASELINE

## Node operations
- health()
- readiness()
- status()
- start()
- stop()
- recover()

## Identity
- identity.status()
- identity.create()
- identity.verify()

## Storage
- storage.create()
- storage.read()
- storage.write()
- storage.delete()
- storage.verify()
- storage.status()

## Engines
- engines.list()
- engines.register()
- engines.start()
- engines.stop()

## Protocols
- protocols.list()
- protocols.validate()
- protocols.install()
- protocols.activate()
- protocols.deactivate()

## Verification
- verify.manifest()
- verify.integrity()
- verify.environment()

The API must expose explicit authorization, state validation and deterministic errors. Sensitive credential material is never returned.
