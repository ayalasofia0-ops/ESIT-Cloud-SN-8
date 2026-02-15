# Diagramas de Arquitectura - Sistema CNDD Storage

## 1. Arquitectura General del Sistema

```mermaid
graph TB
    subgraph "Capa de Usuario"
        U[👤 Usuario Final]
        APP[🌐 Aplicación Web Reflex]
    end

    subgraph "Capa de Autenticación"
        CUP[Amazon Cognito User Pool<br/>- Email/Password<br/>- Grupos de usuarios]
        CIP[Amazon Cognito Identity Pool<br/>- Mapeo a roles IAM]
    end

    subgraph "Capa de Control de Acceso"
        R1[🔍 Rol: Solo Lectura<br/>Ver metadata]
        R2[⬆️ Rol: Solo Carga<br/>Subir archivos]
        R3[⬇️ Rol: Solo Descarga<br/>Descargar archivos]
        R4[✏️ Rol: Lectura/Escritura<br/>CRUD completo]
        R5[👑 Rol: Admin<br/>Acceso total + logs]
    end

    subgraph "Capa de Almacenamiento"
        S1[📁 S3: cndd-publica<br/>🔓 Pública<br/>Lifecycle: 30d → IA, 90d → Glacier]
        S2[📁 S3: cndd-proyectos<br/>🔒 Interna<br/>Lifecycle: 45d → IA, 120d → Glacier]
        S3[📁 S3: cndd-recursoshumanos<br/>🔐 Privada<br/>Lifecycle: 60d → IA, 180d → Glacier]
    end

    subgraph "Capa de Auditoría"
        S4[📝 S3: cndd-logs<br/>Access Logs]
        S5[📋 S3: cndd-cloudtrail-logs<br/>CloudTrail Events]
        CT[☁️ CloudTrail<br/>Captura eventos]
        LM[⚡ Lambda Function<br/>Procesa logs]
        OS[🔍 OpenSearch<br/>Indexa y busca]
    end

    U --> APP
    APP --> CUP
    CUP --> CIP
    CIP --> R1 & R2 & R3 & R4 & R5
    R1 & R2 & R3 & R4 & R5 --> S1 & S2 & S3
    S1 & S2 & S3 -.logs.-> S4
    S1 & S2 & S3 -.eventos.-> CT
    CT --> S5
    S5 -.trigger.-> LM
    LM --> OS
    R5 --> OS

    style U fill:#e1f5ff
    style APP fill:#b3e5fc
    style CUP fill:#fff9c4
    style CIP fill:#fff59d
    style R5 fill:#ffccbc
    style OS fill:#c8e6c9
```

---

## 2. Flujo de Autenticación y Autorización

```mermaid
sequenceDiagram
    participant U as Usuario
    participant APP as App Reflex
    participant CUP as Cognito User Pool
    participant CIP as Cognito Identity Pool
    participant IAM as Rol IAM
    participant S3 as Amazon S3

    U->>APP: 1. Ingresa email/password
    APP->>CUP: 2. Autenticar credenciales
    CUP->>CUP: 3. Verificar en base de datos
    CUP-->>APP: 4. Token JWT + grupo asignado
    
    APP->>CIP: 5. Solicitar credenciales temporales AWS
    Note over CIP: Usuario pertenece al grupo "admin"
    CIP->>IAM: 6. Asumir rol "Cognito-Admin"
    IAM-->>CIP: 7. Credenciales temporales
    CIP-->>APP: 8. Access Key + Secret Key temporal
    
    APP->>S3: 9. Listar archivos (con credenciales temporales)
    S3->>S3: 10. Verificar permisos del rol
    S3-->>APP: 11. Lista de archivos permitidos
    APP-->>U: 12. Mostrar archivos
```

---

## 3. Flujo de Auditoría con OpenSearch

```mermaid
graph LR
    subgraph "Generación de Eventos"
        U[👤 Usuario<br/>Sube archivo]
        S3[📁 S3 Bucket]
    end

    subgraph "Captura"
        CT[☁️ CloudTrail<br/>Registra evento]
        CTB[📋 Bucket CloudTrail<br/>cndd-cloudtrail-logs]
    end

    subgraph "Procesamiento"
        LM[⚡ Lambda<br/>Se activa con S3 trigger]
        PROC[🔄 Procesa JSON.GZ<br/>Extrae datos]
    end

    subgraph "Indexación"
        OS[🔍 OpenSearch<br/>Indexa documento]
        IDX[(📊 Índice:<br/>cloudtrail-logs)]
    end

    subgraph "Visualización"
        DASH[📈 Dashboard<br/>Panel de Admin]
        ADM[👑 Administrador]
    end

    U -->|PutObject| S3
    S3 -.evento.-> CT
    CT -->|Escribe log| CTB
    CTB -->|Trigger| LM
    LM --> PROC
    PROC -->|Index| OS
    OS --> IDX
    IDX --> DASH
    DASH --> ADM

    style U fill:#e1f5ff
    style CT fill:#fff9c4
    style LM fill:#ffccbc
    style OS fill:#c8e6c9
    style DASH fill:#f8bbd0
```

---

## 4. Diagrama de Seguridad por Capas

```mermaid
graph TB
    subgraph "Capa 1: Autenticación"
        A1[✅ Usuario autenticado con Cognito]
        A2[✅ Verificación de email]
        A3[✅ Contraseña segura 8+ caracteres]
    end

    subgraph "Capa 2: Autorización"
        B1[🔐 Grupo de Cognito asignado]
        B2[🔐 Rol IAM mapeado]
        B3[🔐 Política de permisos específica]
    end

    subgraph "Capa 3: Bucket"
        C1[🛡️ Bucket Policy - HTTPS obligatorio]
        C2[🛡️ Solo roles Cognito-*]
        C3[🛡️ Cifrado AES-256 en reposo]
    end

    subgraph "Capa 4: Objeto"
        D1[📝 Versionado habilitado]
        D2[📝 Lifecycle automático]
        D3[📝 Logs de acceso]
    end

    subgraph "Capa 5: Auditoría"
        E1[📊 CloudTrail - Todos los eventos]
        E2[📊 OpenSearch - Búsqueda de anomalías]
        E3[📊 Dashboard - Monitoreo en tiempo real]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3
    B1 --> C1
    B2 --> C2
    B3 --> C3
    C1 --> D1
    C2 --> D2
    C3 --> D3
    D1 --> E1
    D2 --> E2
    D3 --> E3

    style A1 fill:#c8e6c9
    style B1 fill:#fff9c4
    style C1 fill:#ffccbc
    style D1 fill:#b3e5fc
    style E1 fill:#f8bbd0
```

---

## Leyenda de Iconos

- 👤 Usuario
- 🌐 Aplicación Web
- ☁️ Servicios AWS
- 📁 Almacenamiento S3
- 🔍 Solo Lectura
- ⬆️ Solo Carga
- ⬇️ Solo Descarga
- ✏️ Lectura/Escritura
- 👑 Administrador
- ⚡ Procesamiento Lambda
- 📊 Análisis y Búsqueda
- 🔐 Seguridad Alta
- 🔒 Seguridad Media
- 🔓 Seguridad Básica
- ✅ Verificado/Aprobado
- 🛡️ Protección activa
