# Node Core Dual Storage Administrative UI Contract

**Status:** CANONICAL / DESIGN CONTRACT  
**Version:** 1.0.0  
**Scope:** Protocol-neutral administrative presentation of decentralized storage mode.

## Authority

The UI is a presentation and invocation surface only. It MUST delegate mode changes to ConfigurationManager and MUST NOT create a second storage state machine.

## Display model

The storage preferences surface presents:

- Configured mode: LOCAL or DUAL_STORAGE.
- Configured state: the persisted Configuration Manager state.
- Kubo health: HEALTHY or UNHEALTHY.
- Mirror/coherence state: the result of the Kubo coherence verifier when Dual Storage is selected.
- Effective availability: READY or DEGRADED.

The distinction is intentional: `configured mode != effective availability`.

A user may have selected DUAL_STORAGE while Kubo is temporarily degraded. The UI MUST NOT silently rewrite the user's preference to LOCAL.

## Actions

### Select LOCAL

The UI delegates `ConfigurationManager.set_storage_mode("LOCAL")`.

No Kubo coherence gate is required.

### Select DUAL_STORAGE

The UI requests current coherence evidence and delegates `ConfigurationManager.set_storage_mode("DUAL_STORAGE", readiness=coherence_report)`.

If `dual_storage_ready` is false, the UI MUST keep DUAL_STORAGE unavailable and present the reason/state returned by the administrative layer.

## Recovery presentation

When Kubo fails:

`configured_mode = DUAL_STORAGE`
`effective_status = DEGRADED`

The UI MUST communicate that local fallback remains available.

When Kubo recovers, the UI MUST wait for reconciliation and coherence verification before presenting Dual Storage as READY.

## Visual constraints

The first Node Core administrative UI follows the established minimal design:

- white background;
- black primary text;
- dark gray secondary text;
- light gray supporting text;
- clear text hierarchy;
- no decorative background graphics.

The UI must not contain CPG-specific poker controls or protocol logic.
