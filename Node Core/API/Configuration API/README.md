# Configuration API

**Status:** SUPPORTING interface documentation

The canonical configuration authority is `Documentation/Interfaces/NODE-CORE-CONFIGURATION-CONTRACT.md`, implemented by `Configuration/configuration_manager.py` and structurally defined by `Configuration/Schemas/node-configuration.schema.json`.

Controls validated Node Core configuration.

## Contract

- getConfiguration
- validateConfiguration
- stageConfiguration
- activateConfiguration
- rollbackConfiguration
- getConfigurationVersion

Configuration activation must respect the canonical contract, schema validation, integrity requirements and readiness re-evaluation. Protocol installation remains under Protocol Interface.
