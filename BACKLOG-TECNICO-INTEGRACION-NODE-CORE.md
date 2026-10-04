# Backlog técnico de integración

Este backlog traduce la hoja de ruta en trabajo comprobable. Las prioridades son recomendaciones, no compromisos de release.

## P0 — corregir fuente de verdad

### NC-001 — Reconciliar manifiestos y documentación Kubo

**Estado:** pendiente. **Depende de:** ninguno.

Actualizar README y manifiestos Kubo para distinguir capacidades presentes en código, probadas con dobles, no probadas live y no implementadas. Resolver el conflicto sobre recuperación, health, sync y adquisición de releases.

**Aceptación:** los estados de documentos coinciden con el código y la matriz de pruebas; cada declaración de “implemented” cita una prueba y el alcance de esa prueba.

### NC-002 — Definir estados de madurez del proyecto

**Estado:** pendiente. **Depende de:** NC-001.

Adoptar estados inequívocos, por ejemplo `DESIGNED`, `IMPLEMENTED`, `TESTED_LOCAL`, `VERIFIED_LIVE`, `NOT_PROVISIONED` y `NOT_IMPLEMENTED`, sin tratar la presencia de módulos como certificación.

**Aceptación:** Node Core y Kubo usan la misma semántica en manifest, README y salida del gate.

## P1 — reproducibilidad y Kubo live

### NC-010 — Inventariar y declarar dependencias

**Estado:** pendiente. **Depende de:** NC-001.

Separar dependencias runtime, opcionales y dev. Revisar el alcance de `Node Core/Cryptography/requirements.txt` (`cryptography==46.0.4`), identificar dependencias de cada paquete y decidir un runner de pruebas; `pytest` no está instalado actualmente.

**Aceptación:** entorno virtual desde cero instala dependencias fijadas y ejecuta los checks documentados; bibliotecas de referencias vendorizadas no se convierten accidentalmente en dependencias del producto.

### NC-011 — Añadir CI reproducible de Node Core

**Estado:** pendiente. **Depende de:** NC-010.

Automatizar bootstrap en directorio temporal, tests de composición, pruebas Kubo locales, validación de schemas y `final_node_core_audit.py`.

**Aceptación:** CI informa cada gate por separado; fallo o ausencia de pytest no aparece como suite aprobada; artifacts registran Python y plataforma.

### NC-020 — Probar provisionamiento contra Kubo upstream

**Estado:** pendiente. **Depende de:** NC-010 y NC-011.

Ejecutar el resolver y acquirer contra distribución oficial; verificar metadatos, release seleccionado, checksum SHA-512 y límites de tamaño. Conservar versión de release explícita en resultado.

**Aceptación:** Linux `amd64` y `arm64` soportados por el código completan adquisición desde fuente oficial; checksum incorrecto, timeout, metadatos inválidos y paquete sobredimensionado fallan sin dejar instalación activa parcial.

### NC-021 — Completar prueba de ciclo Kubo con daemon real

**Estado:** pendiente. **Depende de:** NC-020.

Provisionar en raíz temporal, inicializar el repo con `IPFS_PATH` absoluto, arrancar daemon, esperar health, comprobar PeerID/versión y detenerlo limpiamente.

**Aceptación:** una prueba Linux automatizada llega a estado saludable con binario real, conserva manifiesto/rutas canónicas y limpia procesos incluso ante fallo; ningún test depende de un daemon compartido del host.

### NC-022 — Verificar Sync, coherencia y fallback live

**Estado:** pendiente. **Depende de:** NC-021.

Ejercitar objetos elegibles, exclusión de datos no distribuibles, recuperación de objeto local ausente, discrepancia remota/local y degradación del provider.

**Aceptación:** dual storage solo entra en `READY` después de health + sync + verificación; conflictos bloquean el gate sin sobrescritura silenciosa; el modo local continúa disponible.

### NC-023 — Formalizar actualización y rollback de Kubo

**Estado:** pendiente. **Depende de:** NC-021.

Definir pin de versión, respaldo del repo/estado, cambio de instalación activa, compatibilidad de repositorio y reversión segura.

**Aceptación:** actualización y rollback ensayados en una instalación disposable; un fallo preserva la versión anterior y sus datos.

## P1 — seguridad de operación

### NC-030 — Endurecer lifecycle del proceso

**Estado:** pendiente. **Depende de:** NC-021.

Antes de detener un PID almacenado, confirmar que pertenece al ejecutable/proveedor esperado; manejar PID obsoleto, proceso sustituido, timeout y escalado de señal. Esperar health antes de reportar startup correcto.

**Aceptación:** pruebas cubren PID reutilizado, daemon que no inicia, daemon que termina durante startup y shutdown con timeout; procesos no relacionados no reciben señales.

### NC-031 — Fijar política de RPC y permisos

**Estado:** pendiente. **Depende de:** NC-021.

Validar que RPC escuche solo en loopback, que no haya gateway/RPC expuesto sin decisión explícita, y que configuración, claves, logs y manifiestos tengan permisos apropiados.

**Aceptación:** test de configuración confirma bind local; checklist de release documenta firewall, autenticación donde aplique y datos sensibles que nunca se registran.

## P2 — interfaces y alcance de plataforma

### NC-040 — Cerrar contratos API y CLI

**Estado:** pendiente. **Depende de:** NC-001 y NC-010.

Conectar status/readiness/start/stop/recover y controles de storage con managers reales, definir códigos de salida y esquemas JSON.

**Aceptación:** pruebas de contrato para éxito, errores y estados degradados; API y CLI no elevan estado antes de sus gates.

### NC-041 — Certificar subsistemas Node Core

**Estado:** pendiente. **Depende de:** NC-011.

Convertir los estados `IMPLEMENTED_PARTIAL` del manifiesto en criterios de aceptación separados para identidad, criptografía, recovery, protocol interface, network, security, time, consensus, engine runtime y node manager.

**Aceptación:** cada subsistema tiene alcance, tests, dependencias y estado; no se eleva globalmente Node Core a completo mientras existan gates requeridos abiertos.

### NC-050 — Integrar CPG como protocolo independiente

**Estado:** pendiente. **Depende de:** NC-040 y especificaciones CPG.

Definir paquete/manifiesto CPG, instalación y ejecución vía Protocol Interface, permisos y almacenamiento separado.

**Aceptación:** tests verifican protocolo instalado/retirado, aislamiento de datos y que reglas de poker/ledger no se incorporan al Node Core.

### NC-060 — Definir soporte Windows/iOS

**Estado:** fuera de la primera entrega Linux. **Depende de:** NC-021.

Crear decisión de plataforma y matriz de binarios, filesystem, daemon, sandbox y CI. Kubo installer actual solo implementa Linux.

**Aceptación:** no se anuncian esas plataformas como soportadas hasta completar instalación, lifecycle y pruebas específicas.

## Secuencia sugerida

`NC-001 → NC-002 → NC-010 → NC-011 → NC-020 → NC-021 → NC-022 → NC-023`

Ejecutar `NC-030` y `NC-031` antes de cualquier uso persistente o expuesto. `NC-040` y `NC-041` avanzan en paralelo después de contratos estables; `NC-050` cierra el producto CPG y `NC-060` amplía plataformas.

## Bloqueos conocidos

- El test runner `pytest` no está presente en el entorno actual.
- El gate de Node Core es local y deja el provider externo sin provisionar.
- La suite Kubo local usa doubles; no acredita comportamiento de upstream ni daemon live.
- `NODE-CORE-MANIFEST.json`, README Kubo y manifiesto Kubo necesitan reconciliación documental.