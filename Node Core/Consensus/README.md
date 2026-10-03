# Node Core Consensus

## Especificación Arquitectónica y Conceptual del Modelo de Consenso Desacoplado

**Proyecto:** Chain Poker Genesis by LAEV  
**Capa:** Node Core  
**Componente:** Consensus  
**Ámbito:** Consenso de infraestructura de nodo  
**Estado:** Especificación arquitectónica y conceptual

---

## 1. Propósito

Node Core/Consensus/ define exclusivamente la arquitectura y los mecanismos del consenso de infraestructura de la Red de Nodos by LAEV.

Este componente permanece desacoplado de Chain Poker Genesis, del consenso de mesa, del estado de poker, del ledger CPG y del settlement.

Su función es establecer condiciones verificables para existencia, elegibilidad, Proof of Function, preferencias operativas, evidencia, participación, consenso colectivo, validación temporal, activación de configuraciones, suspensión y recuperación de elegibilidad, y trazabilidad histórica.

### Frontera

~~~text
Node Core Consensus
        |
        └── Consenso de infraestructura
~~~

No define CPG rules, poker state, table state, CPG ledger ni settlement.

---

## 2. Principio Fundamental

La identidad de un nodo no implica automáticamente participación.

La participación requiere condiciones verificables:

~~~text
Existencia
    ↓
Elegibilidad
    ↓
Proof of Function
    ↓
Preferencia válida
    ↓
Evidencia verificable
    ↓
Consistencia
    ↓
Participación en consenso
~~~

---

## 3. Naturaleza del Consenso

Node Core Consensus utiliza un modelo de consenso por preferencias operativas verificables.

Una preferencia es una opción válida de configuración o estado operativo que el nodo declara estar preparado para ejecutar.

La selección individual de una preferencia no constituye por sí sola consenso. El Consensus Engine transforma las preferencias válidas de los participantes elegibles en un estado colectivo conforme a reglas deterministas.

---

## 4. Filtros de Participación

El modelo utiliza tres filtros secuenciales:

1. Existencia: el nodo puede demostrar una identidad reconocible de la red.
2. Elegibilidad Protocolaria: el nodo satisface las condiciones de participación vigentes.
3. Proof of Function: el nodo demuestra capacidad funcional mediante evidencia verificable.

Solo el conjunto que supera los filtros aplicables forma el universo elegible del proceso.

Cuando una regla establece participación del 100 %, significa el 100 % del universo elegible, no el 100 % de todas las identidades históricas o conocidas.

---

## 5. Proof of Function

Proof of Function demuestra que un nodo puede ejecutar funciones requeridas.

Puede involucrar lectura, escritura, sincronización, propagación, verificación, selección de rutas y otras operaciones definidas mediante manifiestos.

Los manifiestos deben identificar como mínimo función, información requerida, fuentes, rutas válidas, reglas de selección, reglas de ejecución, reglas de verificación y evidencia.

Un nonce o mecanismo equivalente puede proporcionar incertidumbre controlada para seleccionar entre múltiples rutas válidas, manteniendo la prueba verificable.

---

## 6. Preferencias y Consenso

Las preferencias pertenecen a conjuntos de opciones previamente definidos.

Una preferencia válida debe poder asociarse con identidad del nodo, versión, conjunto de opciones, momento de selección, estado de elegibilidad y evidencia correspondiente.

El proceso colectivo debe definir explícitamente validez, conteo, condición de aceptación, empates, conflictos, temporalidad y finalización.

---

## 7. Consistencia y Exclusión

La aceptación de información depende de evidencia y reglas verificables.

Un resultado inválido puede producir pérdida de elegibilidad sin requerir slashing o confiscación económica.

~~~text
Invalid Evidence
      ↓
Verification Failure
      ↓
Eligibility Failure
      ↓
Excluded from Participation
~~~

---

## 8. Tiempo y Activación

Consensus utiliza referencias temporales para vigencia, orden, preparación, activación, expiración y reconstrucción histórica.

El reloj local no constituye por sí mismo autoridad de consenso.

Las configuraciones pueden activarse mediante Activation Height o Activation Timestamp.

Ciclo conceptual:

~~~text
PROPOSED
   ↓
ANNOUNCED
   ↓
PREPARATION
   ↓
SELECTION
   ↓
LOCKED
   ↓
SCHEDULED
   ↓
ACTIVATED
   ↓
ENFORCED
   ↓
RETIRED
~~~

---

## 9. Suspensión y Recuperación

La pérdida de elegibilidad no destruye el Node Core.

~~~text
Node Core = RUNNING
Consensus Eligibility = SUSPENDED
~~~

El nodo puede volver a ser elegible después de satisfacer nuevamente los requisitos de configuración, compatibilidad y Proof of Function.

---

## 10. Determinismo

Bajo las mismas entradas, reglas y contexto, los nodos deben producir el mismo resultado.

~~~text
Same Inputs
+
Same Rules
+
Same Context
=
Same Result
~~~

---

## 11. Estructura

- Consensus Engine — coordinación del consenso.
- Consensus Rules — reglas normativas.
- Eligibility — filtros de elegibilidad.
- Participation — estados de participación.
- Proof of Function — pruebas funcionales.
- Manifests — manifiestos canónicos.
- Preference Voting — selección de preferencias.
- Policy Consensus — consenso de políticas operativas.
- Evidence — evidencia y trazabilidad.
- Conflict Resolution — conflictos.
- Temporal Activation — activación temporal.
- State — estados e invariantes.
- Propagation Control — control de propagación.
- Propagation Verification — verificación de propagación.
- Request Verification — validación de solicitudes.
- State Verification — validación de estados.
- Synchronization Verification — verificación de sincronización.
- Versioning — versiones y ciclo de vida.

---

## 12. Estado de Implementación

Este README define arquitectura y modelo conceptual. No declara implementados los algoritmos que todavía requieren especificación formal.

Ruta prevista:

~~~text
CONCEPT
   ↓
FORMAL SPECIFICATION
   ↓
INTERFACES
   ↓
STATE MACHINES
   ↓
CANONICAL SCHEMAS
   ↓
TEST VECTORS
   ↓
REFERENCE IMPLEMENTATION
   ↓
IMPLEMENTATION VERIFICATION
~~~

El algoritmo exacto, aceptación, conflictos, finalización, particiones, fallos, mensajes, persistencia, Proof of Function, preferencias, activación y recuperación deberán formalizarse antes de declarar Consensus completamente implementado.

---

## 13. Frontera Arquitectónica

Node Core Consensus permanece desacoplado de cualquier protocolo superior.

Los protocolos superiores pueden consumir sus servicios mediante interfaces, pero no deben introducir semántica específica de aplicación dentro de este componente.

**Node Core Consensus = consenso de infraestructura.**
