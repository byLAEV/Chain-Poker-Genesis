# Especificaciones y Manuales para Desarrolladores

Esta carpeta concentra las especificaciones técnicas y manuales destinados al equipo de desarrollo del repositorio **Chain Poker Genesis by LAEV** y de las capas de infraestructura que lo soportan.

## Estructura base

```text
docs/
└── developer-specifications/
    ├── README.md
    ├── storage/
    │   └── README.md
    ├── identity/
    ├── synchronization/
    ├── consensus/
    ├── recovery/
    ├── security/
    ├── engines/
    ├── APIs/
    ├── testing/
    └── integration/
```

Las carpetas futuras se incorporarán mediante sus respectivos manuales README, evitando mezclar infraestructura transversal con motores y aplicaciones superiores.

## Separación arquitectónica

```text
RED DE NODOS BY LAEV
        │
        ├── Storage Infrastructure
        ├── Cryptographic Identity
        ├── Identity Synchronization
        ├── SREC / Recovery
        └── Consensus Engine
                │
                ▼
        CHAIN POKER GENESIS
        ├── Poker Engines
        ├── Wallet Engines
        ├── Settlement Engines
        └── Application Components
```

Las especificaciones de infraestructura de la Red de Nodos by LAEV deben permanecer independientes de Chain Poker Genesis. Los protocolos y motores superiores consumen estas capacidades mediante APIs y contratos definidos.

## Directorios documentales

- `storage/` — almacenamiento local, metadata, políticas, sincronización, recuperación e integración Kubo/IPFS.
- `identity/` — identidad criptográfica del nodo.
- `synchronization/` — sincronización y distribución.
- `consensus/` — coordinación y consenso entre nodos.
- `recovery/` — recuperación, continuidad y respaldos.
- `security/` — seguridad transversal.
- `engines/` — especificaciones de motores instalables.
- `APIs/` — contratos de interfaces entre capas.
- `testing/` — pruebas y criterios de aceptación.
- `integration/` — integración entre infraestructura, motores y aplicaciones.

## Estado

Esta estructura constituye la base documental para desarrollar las especificaciones formales antes de implementar cada componente.
