# Plan de integración Kubo/IPFS y dependencias

## Estado observado

Los módulos Kubo existentes cubren resolución de versión y artefactos, adquisición con SHA-512, extracción segura, inicialización del repositorio, lifecycle del proceso, health, sincronización inicial, coherencia, reconciliación y recuperación. Se ejecutaron 31 funciones de prueba locales, incluyendo casos de checksum incorrecto, traversal de archivos, conflicto y fallback.

Esto demuestra comportamiento local con dobles, no una instalación real. El gate actual mantiene `external_provider = NOT_PROVISIONED`, `synchronization = NOT_EVALUATED` y la línea base local de Node Core como completion gate. El README de Kubo está desactualizado frente al código y al manifiesto; resolverlo forma parte del plan.

## Contrato de almacenamiento y ownership

- Node Core mantiene almacenamiento local como base canónica y fallback.
- Kubo es un provider opcional; no debe instalarse silenciosamente como requisito del bootstrap.
- Las rutas bajo raíz del nodo son: `External Providers/Kubo/<version>/` para instalación y `node-storage/providers/kubo/{repository,runtime,logs,state,synchronization}/` para estado operativo.
- `IPFS_PATH` debe ser absoluto y apuntar al repo administrado, no al home del usuario ni a un repo compartido.
- CPG conserva sus propios datos y semánticas; provider/IPFS no redefine el ledger ni el estado del protocolo.
- Dual Storage solo puede declararse `READY` con provider instalado, repo inicializado, health válido, sync completa, integridad y sin conflictos sin resolver.

## Flujo de provisionamiento requerido

1. **Preflight:** validar Linux/arquitectura (`amd64` o `arm64`), espacio, permisos, root y ausencia de instalación incompatible.
2. **Selección:** resolver release estable desde fuente oficial; guardar versión explícita, URL, plataforma y metadatos utilizados. “Latest” se resuelve una sola vez por provisión; upgrades son explícitos.
3. **Adquisición:** obtener artefacto y sidecar SHA-512 desde host oficial, con timeout y límite de tamaño. No activar paquete parcial.
4. **Verificación:** comparar digest, validar nombre/tipo/formato y registrar digest/version en manifest activo. Rechazar checksum ausente o discrepante.
5. **Instalación:** extraer en staging, rechazar path traversal y enlaces no admitidos, validar ejecutable y promover atómicamente a directorio versionado.
6. **Repositorio:** derivar rutas con `KuboPathManager`, pasar `IPFS_PATH` absoluto al proceso `ipfs init`, validar config, PeerID y versión; no reinicializar un repositorio existente.
7. **Arranque:** lanzar daemon con logs controlados, guardar proceso/versión/rutas y esperar health hasta timeout. Validar identidad del proceso antes de señalizarlo al parar.
8. **Health y red:** comprobar endpoints locales de identidad y versión; asegurar que RPC no queda expuesto fuera de loopback sin decisión de seguridad explícita.
9. **Sync inicial:** reconciliar objetos distributables desde registro local, verificar integridad y estados de cada objeto; reportar explícitamente omitidos, reparados y conflictos.
10. **Activación:** emitir `READY` para Dual Storage solo si todos los requisitos canónicos se cumplen. En fallo, dejar provider `DEGRADED`/`FAILED` y mantener lectura/escritura local según política, sin ocultar conflicto.
11. **Operación:** implementar stop/restart, recuperación, actualización, rollback, limpieza de temporales y auditoría de logs/manifiesto.

## Dependencias

### Runtime

- Python 3.9 o posterior es el mínimo declarado por el bootstrap.
- Los módulos Bootstrap y Kubo revisados usan biblioteca estándar de Python (`urllib`, `hashlib`, `tarfile`, `zipfile`, `subprocess`, `pathlib`, entre otras).
- El binario Kubo es un artefacto externo por plataforma, no un paquete Python; la instalación debe verificar el artefacto upstream y conservar su versión.
- Existe `Node Core/Cryptography/requirements.txt` con `cryptography==46.0.4`. Determinar qué componentes la importan y si su alcance seguirá siendo local o se moverá a un manifiesto común.

### Desarrollo/CI

- `pytest` no está instalado en el entorno observado. Definir si se convierte en dependencia de desarrollo o si se estandariza `unittest`; no declarar ejecutada una suite que requiere un runner ausente.
- Inventariar lint, schema validation y dependencias de tests; excluir árboles `External References`, `Core References` y `node_modules` salvo que una dependencia vendorizada forme explícitamente parte del producto.
- Fijar versiones de herramientas en CI y documentar una instalación limpia con `venv`.

### Mapa de manifiestos

- [Manifiesto del instalador Kubo](Node%20Core/Documentation/Storage/Kubo/KUBO-NODE-INSTALLER-MANIFEST.json): lifecycle, rutas, policy y test vectors.
- [Manifiesto upstream](Node%20Core/Documentation/Storage/Kubo/KUBO-UPSTREAM-MANIFEST.json): ownership, capacidades requeridas y activación de dual storage.
- [Esquema de manifiesto activo](Node%20Core/Documentation/Storage/Kubo/KUBO-ACTIVE-MANIFEST-SCHEMA.json): identidad y digest de instalación.
- [Código Kubo](Node%20Core/Storage/Kubo/README.md): debe actualizarse para representar las capacidades presentes y sus límites live.

## Matriz de verificación

| Capa | Prueba local actual | Prueba live pendiente |
|---|---|---|
| Release metadata | URLs/selección con respuestas simuladas | Consulta oficial y schema/compatibilidad real |
| SHA-512 | Digest correcto e incorrecto con bytes de prueba | Descarga real, sidecar real, timeout y reintento |
| Installer | Paquete sintético; traversal y digest alterado rechazados | Binario oficial y checksum de release |
| Repo | Init/path/validación con ejecutable de prueba | `ipfs init` real, PeerID y versión |
| Process/health | PID obsoleto, precondiciones y health simulado | Start/stop real, timeout, bind RPC y proceso sustituido |
| Sync/coherence | Provider fake, reparación, conflicto y fallback | Repo real con datos persistidos y recuperación post-restart |
| Dual Storage | Gate lógico local | Persistencia de READY, degradación y retorno seguro a local |

## Criterio de aprobación Kubo

Kubo queda **verificado para Linux** únicamente cuando una prueba aislada desde cero completa provisión, verificación de artefacto, init, daemon, health, sync, coherencia, apagado y reinicio; el digest y versión quedan en manifiesto; no hay exposición RPC inesperada; y el test confirma que no se activa Dual Storage con conflictos o sincronización incompleta.

Hasta entonces, reportar con precisión: **“código Kubo parcialmente implementado y cubierto por pruebas locales; provider live no provisionado ni certificado”**. La plataforma Windows/iOS queda fuera de la primera certificación hasta contar con instalador, proceso, pruebas y CI equivalentes.

## Referencias

- [Hoja de ruta](HOJA-DE-RUTA-INTEGRACION-NODE-CORE.md)
- [Backlog técnico](BACKLOG-TECNICO-INTEGRACION-NODE-CORE.md)
- [Informe de auditoría](AUDITORIA-NODE-CORE-CHAIN-POKER-GENESIS.md)
- [Manifiesto Node Core](Node%20Core/NODE-CORE-MANIFEST.json)