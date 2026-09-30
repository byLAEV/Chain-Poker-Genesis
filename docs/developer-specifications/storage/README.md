# Infraestructura de Almacenamientos de la Red de Nodos by LAEV

**Documento:** Especificación técnica de arquitectura y desarrollo  
**Versión:** 1.1  
**Estado:** Base de desarrollo  
**Ámbito:** almacenamiento, clasificación, integridad, persistencia, sincronización, recuperación e integración con Kubo/IPFS  
**Propietario conceptual:** Red de Nodos by LAEV  
**Dependencias superiores:** Ninguna aplicación o protocolo específico

## Propósito

La infraestructura de almacenamiento es una capa transversal e independiente para módulos, aplicaciones, motores y protocolos instalados posteriormente sobre la Red de Nodos by LAEV. No depende de Chain Poker Genesis.

## Arquitectura

```text
Application / Engine
        │
        ▼
   Storage API
        │
        ▼
 Storage Manager
   ┌────┴────┐
   ▼         ▼
Policy     Metadata
Engine
   │
   ├── Local Storage
   ├── Synchronization
   ├── Recovery
   └── Distributed Adapter
             │
             ▼
        Kubo Adapter
             │
             ▼
            Kubo
             │
             ▼
            IPFS
```

## Estructura principal

```text
NODE/
├── storage/
├── services/
├── applications/
├── config/
├── runtime/
└── logs/
```

```text
storage/
├── local/
├── synchronization/
├── distributed/
├── metadata/
└── recovery/
```

```text
storage/local/
├── system/
├── shared/
├── modules/
├── temporary/
├── public/
├── private/
├── restricted/
├── personal/
└── backup/
```

```text
storage/synchronization/
├── outgoing/
├── incoming/
├── pending/
├── processing/
├── published/
├── failed/
├── retry/
├── quarantine/
└── manifests/
```

## Principios obligatorios

1. **Separación de responsabilidades:** Storage API, Storage Manager, Policy Engine, Local Storage, Synchronization, Metadata, Kubo Adapter y Kubo/IPFS son componentes diferenciados.
2. **Almacenamiento local independiente:** el estado local válido debe continuar disponible aunque Kubo, IPFS o una cola de sincronización estén indisponibles.
3. **Almacenar no equivale a sincronizar:** la distribución debe ser resultado explícito de una política.
4. **Integridad independiente de ubicación:** un objeto debe poder verificarse localmente, en Kubo/IPFS o durante recuperación.
5. **Aislamiento de módulos:** un módulo no escribe directamente en el almacenamiento privado de otro módulo.
6. **Kubo encapsulado:** nunca se escribe directamente en el repositorio interno de Kubo; se utiliza su API/RPC mediante un adaptador.
7. **Storage no es consenso:** almacenamiento, identidad, sincronización y consenso permanecen separados.

## Clases de almacenamiento

- `TEMPORARY`
- `LOCAL_PUBLIC`
- `LOCAL_PRIVATE`
- `LOCAL_RESTRICTED`
- `LOCAL_PERSONAL`

`LOCAL_PUBLIC` no implica publicación automática en IPFS. `LOCAL_RESTRICTED` debe tener sincronización desactivada por defecto y controles adicionales.

## API y componentes

Todo módulo superior utiliza una API unificada, conceptualmente:

```text
StorageManager.put(object, policy)
```

El Storage Manager coordina como mínimo:

```text
CREATE READ UPDATE DELETE
CLASSIFY STORE RETRIEVE VERIFY
PREPARE_SYNC PUBLISH RECEIVE
QUARANTINE RESTORE BACKUP
```

El Policy Engine debe poder expresar como mínimo:

```text
WHERE
WHO
WHEN
HOW LONG
ENCRYPTED
SYNC
PIN
REPLICATE
DELETE
```

## Modelo de objeto

```text
Object
├── object_id
├── module_id
├── version
├── local_location
├── content_hash
├── cid
├── storage_class
├── visibility
├── encryption
├── persistence
├── sync_policy
├── retention_policy
├── replication_policy
├── object_state
├── sync_state
└── distributed_state
```

Los identificadores `object_id`, `operation_id`, `version`, `content_hash` y `CID` tienen funciones distintas. UUIDv4 no es determinista. Dos objetos lógicos pueden compartir legítimamente el mismo CID; debe evitarse la duplicación lógica accidental, no la reutilización de contenido.

## Manifest y consistencia

El manifiesto es el registro durable que relaciona objeto, almacenamiento local, integridad, sincronización, distribución y versión. Las carpetas operativas (`pending`, `processing`, `published`, `failed`, `retry`, `quarantine`, etc.) no son por sí solas la fuente de verdad.

La consistencia entre filesystem, Metadata Store, Kubo e IPFS debe manejarse mediante operaciones durables, estados, recuperación, reconciliación, reintentos y verificación posterior; no debe asumirse una transacción única entre todos esos sistemas.

## Estados

Separar como mínimo:

```text
OBJECT_STATE
SYNC_STATE
DISTRIBUTED_STATE
```

Ciclo mínimo:

```text
CREATED → CLASSIFIED → STORED_LOCAL
                         │
                         ├── NO_SYNC
                         │
                         └── SYNC_PENDING → SYNC_PROCESSING → DISTRIBUTED
                                                   │
                                                   └→ RETRY_WAIT

INVALID → QUARANTINED
```

## Sincronización y fallos

Las colas deben ser durables y registrar `operation_id`, `attempt`, `next_retry_at`, `last_error`, `backoff`, `created_at` y `updated_at`. Deben utilizarse backoff exponencial, jitter, clasificación de errores, límite de intentos, backpressure y circuit breaker.

Una cola saturada no debe bloquear necesariamente el almacenamiento local.

## Integridad, cifrado y red

Debe mantenerse la separación:

```text
CID ≠ Encryption Key
CID ≠ Permission
CID ≠ Identity
CID ≠ Authorization
IPFS ≠ Encryption
PIN ≠ Consensus
Replication ≠ Backup
Sync ≠ Replication
```

`IPFS_PUBLIC_NETWORK` e `IPFS_PRIVATE_NETWORK` son propiedades distintas de `CONTENT_ENCRYPTION` y `ACCESS_POLICY`. Los datos sensibles deben cifrarse antes de distribuirse cuando la política lo requiera.

## Persistencia y distribución

Diferenciar:

```text
STORED
PINNED
PROVIDED / ANNOUNCED
REPLICATED
```

Las políticas de replicación pueden ser `LOCAL_ONLY`, `MULTI_NODE` o `EXTERNAL_PINNING`.

## Kubo

Kubo se integra como servicio especializado:

```text
Storage API
 → Storage Manager
 → Distributed Adapter
 → Kubo Adapter
 → Kubo API/RPC
 → Kubo Repository
 → IPFS
```

El repositorio interno de Kubo pertenece a Kubo y no debe ser utilizado como base de datos de la aplicación. La infraestructura mantiene sus propios metadatos, manifiestos, políticas y estados.

## Recuperación y degradación

Tras un reinicio o fallo, el estado debe reconstruirse mediante metadata, registros de operaciones, inspección del filesystem y verificación de Kubo/IPFS.

Ejemplo:

```text
Kubo OFFLINE
    ↓
Local storage continues
    ↓
Sync queue accumulates
    ↓
Retry policy
    ↓
Kubo returns
    ↓
Synchronization resumes
```

Las operaciones deben ser reconciliables para resolver fallos parciales como publicación completada sin confirmación local o actualización de manifest fallida después de una escritura.

## Backup y recuperación

El backup es una política independiente de sincronización, replicación, pinning y publicación IPFS:

```text
BACKUP ≠ REPLICATION
BACKUP ≠ SYNC
BACKUP ≠ PINNING
```

## Concurrencia, idempotencia y versionado

La implementación debe definir locking o concurrencia optimista, comprobación de versión y orden de operaciones. No se permiten sobrescrituras silenciosas.

Las operaciones deben ser idempotentes cuando sea posible. Un objeto lógico puede mantener múltiples versiones y cada versión conserva su `content_hash`, CID, metadata, fecha y historial de operaciones.

## Seguridad

Separar explícitamente:

```text
IDENTITY
AUTHENTICATION
AUTHORIZATION
ENCRYPTION
INTEGRITY
STORAGE POLICY
```

No se permite publicación automática de secretos o material criptográfico.

## Observabilidad

El sistema debe permitir responder qué objeto existe, dónde está, qué versión representa, cuál es su hash/CID, si fue sincronizado/publicado/pinned/replicado, cuándo ocurrió la última operación y por qué falló un intento.

Los logs son evidencia operacional, pero no sustituyen al Metadata Store ni a los registros durables.

## Criterios mínimos de aceptación

```text
[ ] Storage API
[ ] Storage Manager
[ ] Policy Engine
[ ] Local Storage aislado
[ ] Metadata durable
[ ] object_id
[ ] Versionado
[ ] content_hash
[ ] Manifest
[ ] State Machine
[ ] Estados separados object/sync/distributed
[ ] Cola de sincronización
[ ] Retry + backoff + jitter
[ ] Control de saturación
[ ] Recovery
[ ] Quarantine
[ ] Kubo Adapter
[ ] Sin escritura directa al Kubo Repository
[ ] Stored/Pinned/Provided/Replicated diferenciados
[ ] Cifrado separado de red IPFS
[ ] CID separado de identidad
[ ] Aislamiento entre módulos
[ ] Trazabilidad
[ ] Degradación controlada
```

## Estado del documento

Esta especificación constituye el **baseline de desarrollo** de la Infraestructura de Almacenamientos de la Red de Nodos by LAEV y debe evolucionar mediante versiones documentadas antes de introducir cambios arquitectónicos.
