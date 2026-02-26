# CNDD Project - Sistema de Gestión de Archivos S3

Sistema de almacenamiento centralizado en AWS con control de acceso multi-rol y auditoría completa.

**Proyecto de práctica profesional** - Cloud Computing  
**Autor:** Luis Eduardo Ayala Rayas | Luis Martel  
**Institución:** ESIT - Estancia Profesional  
**Semestre:** 03-25

---

## 📖 Descripción

Este proyecto implementa un sistema empresarial de gestión documental usando servicios de AWS. Simula cómo una organización puede gestionar archivos de forma segura en la nube, con diferentes niveles de acceso según departamentos y roles.

**Características principales:**
- ✅ Autenticación segura con AWS Cognito
- ✅ 5 roles de usuario con permisos granulares
- ✅ Gestión completa de archivos (upload, download, delete)
- ✅ 4 buckets S3 con diferentes niveles de seguridad
- ✅ Auditoría completa con CloudTrail + OpenSearch
- ✅ Interfaz web moderna con Reflex

---

## 👥 Roles de Usuario

| Rol | Buckets | Listar | Subir | Descargar | Eliminar | Admin |
|-----|---------|--------|-------|-----------|----------|-------|
| **Admin** | Todos (4) | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Lectura-Escritura** | Pública, Proyectos | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Solo-Lectura** | Pública | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Solo-Carga** | Pública, Proyectos | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Solo-Descarga** | Pública, Proyectos | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## 🏗️ Arquitectura
```
┌─────────────┐
│  Usuario    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Amazon Cognito  │  ◄── Autenticación + Autorización
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Roles  │  ◄── Control de acceso (IAM)
    │  IAM   │
    └────┬───┘
         │
         ▼
┌─────────────────┐
│   Amazon S3     │  ◄── Almacenamiento
│  - cndd-publica      │
│  - cndd-proyectos    │
│  - cndd-rrhh         │
│  - cndd-logs         │
└────────┬────────┘
         │
         ▼
    ┌───────────┐
    │CloudTrail │  ◄── Auditoría de eventos
    │  + Lambda │
    └─────┬─────┘
          │
          ▼
    ┌────────────┐
    │ OpenSearch │  ◄── Búsqueda y análisis de logs
    └────────────┘
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.9+
- AWS CLI configurado
- Node.js 16+ (para Reflex)
- Cuenta AWS activa

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/ayalasofia0-ops/ESIT-Cloud-SN-8.git
cd ESIT-Cloud-SN-8
```

2. **Crear entorno virtual:**
```bash
python -m venv esit
esit\Scripts\activate  # Windows
source esit/bin/activate  # Linux/Mac
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**

Crea un archivo `.env` en la raíz con:
```env
# AWS General
AWS_REGION=us-east-2

# Cognito
COGNITO_USER_POOL_ID=us-east-2_XXXXXXXXX
COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXX
COGNITO_IDENTITY_POOL_ID=us-east-2:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

# S3 Buckets
BUCKET_PUBLICA=cndd-publica
BUCKET_PROYECTOS=cndd-proyectos
BUCKET_RRHH=cndd-rrhh
BUCKET_LOGS=cndd-logs

# OpenSearch
OPENSEARCH_ENDPOINT=search-cndd-opensearch-xxxxx.us-east-2.es.amazonaws.com
OPENSEARCH_INDEX_NAME=cloudtrail-logs
OPENSEARCH_MASTER_USER=admin
OPENSEARCH_MASTER_PASSWORD=tu-password-segura
```

5. **Ejecutar la aplicación:**
```bash
reflex run
```

6. **Acceder:**
```
http://localhost:3000
```

---

## 📖 Uso

### Iniciar sesión

- **URL:** http://localhost:3000/login
- **Email:** Tu email configurado en Cognito
- **Password:** Tu contraseña

### Funcionalidades por rol

**Todos los usuarios:**
- Dashboard personalizado con nombre
- Ver archivos en buckets permitidos

**Roles con permisos de carga:**
- Subir archivos (con diálogo de confirmación)

**Roles con permisos de descarga:**
- Descargar archivos (descarga automática)

**Roles con permisos de eliminación:**
- Eliminar archivos (con confirmación)

**Solo Admin:**
- Crear usuarios con nombre completo
- Ver logs de CloudTrail en tiempo real
- Acceso a todos los buckets

---

## 🔐 Seguridad

### Implementado:

- ✅ Cifrado en tránsito (HTTPS)
- ✅ Cifrado en reposo (AES-256)
- ✅ Versionado de objetos
- ✅ Lifecycle policies
- ✅ Auditoría completa con CloudTrail
- ✅ Principio de mínimo privilegio (IAM)
- ✅ URLs pre-firmadas con expiración (5 min)
- ✅ Logout seguro (invalida tokens)

---

## 🛠️ Tecnologías

**AWS Cloud:**
- Amazon S3 (almacenamiento)
- Amazon Cognito (autenticación)
- AWS IAM (control de acceso)
- CloudTrail (auditoría)
- AWS Lambda (procesamiento)
- OpenSearch (búsqueda de logs)

**Desarrollo:**
- Python 3.11
- Reflex 0.8.26 (framework web)
- boto3 1.42.17 (AWS SDK)
- opensearch-py 3.1.0

---

## 📂 Estructura del Proyecto
```
ESIT-Cloud-SN-8/
├── .env                    # Variables de entorno
├── rxconfig.py             # Configuración de Reflex
├── requirements.txt        # Dependencias Python
├── README.md              # Este archivo
├── CNDD_Project/          # Aplicación principal
│   ├── CNDD_Project.py    # App Reflex
│   ├── state.py           # Estado global
│   ├── pages/             # Páginas de la app
│   │   ├── login.py       # Autenticación
│   │   ├── dashboard.py   # Panel principal
│   │   ├── files.py       # Gestión de archivos
│   │   └── admin.py       # Panel admin
│   ├── components/        # Componentes reutilizables
│   │   └── navbar.py      # Barra de navegación
│   └── utils/             # Utilidades
│       ├── aws_cognito.py # Autenticación Cognito
│       ├── s3_manager.py  # Operaciones S3
│       └── opensearch_client.py  # Cliente OpenSearch
├── aws_config/            # Configuraciones AWS
│   ├── policies/          # Políticas IAM
│   ├── cognito/           # Config Cognito
│   ├── cloudtrail/        # Config CloudTrail
│   └── lambda/            # Funciones Lambda
├── scripts/               # Scripts de automatización
└── docs/                  # Documentación adicional
```

---

## 💰 Costos Estimados (AWS)

Para uso de desarrollo/demostración:

| Servicio | Costo mensual |
|----------|---------------|
| S3 | ~$0.50 (primeros 5GB gratis) |
| Cognito | Gratis (hasta 50,000 usuarios) |
| CloudTrail | ~$2.00 |
| OpenSearch | ~$15.00 (instancia t3.small) |
| Lambda | Gratis (nivel gratuito) |
| **TOTAL** | **~$17-20/mes** |

💡 **Tip:** Apagar OpenSearch cuando no se use para reducir costos.

---

## ⚠️ Problemas Conocidos

- OpenSearch tarda ~15 minutos en iniciar la primera vez
- Los logs de CloudTrail pueden tardar hasta 15 minutos en aparecer en OpenSearch
- Cognito requiere verificación de email (revisar spam si no llega)
- El primer `reflex run` tarda 3-5 minutos instalando Node.js/npm

---

## 🔮 Próximas Mejoras

- [ ] Compartir archivos entre usuarios
- [ ] Notificaciones por email
- [ ] Vista previa de archivos (PDF, imágenes)
- [ ] Barra de progreso en uploads
- [ ] Paginación en lista de archivos
- [ ] Búsqueda avanzada por fechas en logs
- [ ] App móvil

---

## 👨‍💻 Autores

**Luis Enrique Muñoz Martel | Luis Martel** \
**Karla Sofia Ayala Quijada | Karla Ayala**\
**Edwin Fernando Sanchez Pineda | Edwin Pineda**\
**Melvin Omar Juarez Rodriguez | Melvin Juarez**  
Estudiantes de Tecnico Superior en Servicios en la Nube  
ESIT - Estancia Profesional  
Semestre: 03-25

---

## 🙏 Agradecimientos

Gracias al tutor y compañeros por el apoyo durante el desarrollo de este proyecto.

---

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.

---

**⚠️ Nota:** Este proyecto fue desarrollado con fines académicos. No se recomienda usar en producción sin una revisión exhaustiva de seguridad.