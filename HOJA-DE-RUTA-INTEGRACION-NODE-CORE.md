# Hoja de ruta de integración de Node Core

## Propósito

Definir el orden de trabajo para pasar de la línea base local verificada a un Node Core reproducible y, posteriormente, a una instalación completa de Chain Poker Genesis (CPG). Esta hoja de ruta no afirma que las fases pendientes estén implementadas.

## Punto de partida verificado

- El bootstrap crea y valida una instalación limpia de Node Core.
- Las cinco pruebas de composición pasan; el gate end-to-end informa `audit_status = PASS` y `completion_gate = NODE_CORE_IMPLEMENTATION_BASELINE`.
- El protocolo CPG permanece `NOT_INSTALLED`, de acuerdo con el límite protocol-neutral declarado por Node Core.
- Treinta y una funciones de prueba Kubo pasaron con proveedores/respuestas locales simulados. No se ha validado un daemon Kubo real.
- El gate informa `external_provider = NOT_PROVISIONED` y `synchronization = NOT_EVALUATED`.
- No hay manifiesto de dependencias único para Node Core; existe un manifiesto de Cryptography y no está instalado `pytest` en este entorno.

La evidencia y limitaciones se mantienen en [el informe de auditoría](AUDITORIA-NODE-CORE-CHAIN-POKER-GENESIS.md).

## Fases y criterios de salida

### Fase 0 — Normalizar la fuente de verdad

**Trabajo:** reconciliar `NODE-CORE-MANIFEST.json`, los manifiestos Kubo y sus README con el código y las pruebas; clasificar estados como diseñado, implementado, probado localmente y validado live.

**Salida:** cada afirmación de estado apunta a un test o a una evidencia de ejecución; no hay contradicciones entre manifest, README y gate.

### Fase 1 — Entorno reproducible

**Trabajo:** inventariar imports de producción y tests; separar dependencias de runtime, opcionales y desarrollo; definir versiones soportadas, entorno virtual y comando único de validación. Conservar `cryptography==46.0.4` en su alcance actual hasta decidir si debe pasar a la dependencia común.

**Salida:** instalación limpia documentada, dependencias declaradas sin referencias vendorizadas mezcladas con las del producto y CI ejecutando bootstrap, tests y auditorías desde cero.

### Fase 2 — Proveedor Kubo real (Linux)

**Trabajo:** ejecutar el lifecycle existente contra la distribución oficial y un binario real; confirmar arquitectura, SHA-512, rutas, init, health, sincronización y reconciliación. Añadir un flujo reproducible de provisionamiento y documentar upgrade/rollback.

**Salida:** prueba Linux aislada completa desde release hasta `READY`, sin dobles de Kubo; persistencia correcta del manifiesto activo; provider apagado devuelve fallback local y no pierde datos.

### Fase 3 — Seguridad y operación

**Trabajo:** asegurar RPC ligado solo a loopback, validar el proceso antes de enviar señales desde PID guardado, implementar espera/timeout de health durante startup, proteger permisos de secretos/estado y probar apagado/recuperación.

**Salida:** pruebas de seguridad y fallos pasan; ningún estado declara `READY` con proceso muerto, RPC inaccesible, sincronización incompleta o conflictos pendientes.

### Fase 4 — Contratos API/CLI y servicios del nodo

**Trabajo:** convertir los manifiestos parciales de API y CLI en contratos ejecutables; probar comandos de ciclo de vida, almacenamiento, estado y recuperación. Completar validación de identidad, criptografía, red, tiempo, seguridad y runtime según su propio alcance.

**Salida:** contratos versionados, errores y estados estables, pruebas de integración entre API/CLI y managers; ningún componente se declara completo por la sola presencia de archivos.

### Fase 5 — Integración de CPG

**Trabajo:** implementar CPG como protocolo independiente mediante Protocol Interface; especificar instalación, permisos, estado de protocolo, servicios Node Core requeridos y pruebas de aislamiento.

**Salida:** ciclo del protocolo probado sin trasladar reglas de poker/ledger a Node Core; los estados del manifiesto identifican explícitamente si CPG no está instalado, instalado o ejecutándose.

### Fase 6 — Certificación de release

**Trabajo:** ejecutar matriz limpia en las plataformas soportadas, auditorías, recuperación, upgrades, almacenamiento local/dual y protocolo; generar artefactos y reporte de release.

**Salida:** gate de release reproducible y firmado por evidencia; limitaciones conocidas publicadas. No llamar “integrado completamente” al sistema hasta que los gates de Node Core, proveedor requerido y protocolo estén aprobados.

## Orden de dependencias

`Fase 0 → Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 5 → Fase 6`

Fase 4 puede avanzar en paralelo con la Fase 2 cuando los contratos estén normalizados. CPG no debe bloquear el uso de Node Core como infraestructura neutral, pero sí es requisito para certificar el producto CPG completo.

## Gates de aceptación

| Gate | Requisito mínimo | Estado actual |
|---|---|---|
| Node Core baseline | Bootstrap, verificador y gate local pasan en raíz temporal limpia | Aprobado en la ejecución actual |
| Kubo local tests | Pruebas de lifecycle con dobles | 31 funciones aprobadas; no sustituye prueba live |
| Kubo live | Descarga verificada, instalación, repo, daemon, health y sync reales | Pendiente |
| Dual storage | Sync completa, integridad y reconciliación sin conflicto | Solo lógica probada localmente; no activado en instalación actual |
| API/CLI | Contratos y operaciones verificadas de punta a punta | Parcial |
| CPG | Instalación y ciclo protocol-neutral aislado | No instalado |
| Release completo | Todos los gates aplicables y reproducibles | Pendiente |

## Documentos relacionados

- [Backlog técnico](BACKLOG-TECNICO-INTEGRACION-NODE-CORE.md)
- [Plan Kubo/IPFS y dependencias](PLAN-INTEGRACION-KUBO-IPFS-Y-DEPENDENCIAS.md)
- [Manifiesto Node Core](Node%20Core/NODE-CORE-MANIFEST.json)
- [Manifiesto de instalación Kubo](Node%20Core/Documentation/Storage/Kubo/KUBO-NODE-INSTALLER-MANIFEST.json)