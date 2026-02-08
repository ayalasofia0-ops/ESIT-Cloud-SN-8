# Sistema de Almacenamiento Centralizado en AWS S3

Proyecto de práctica profesional desarrollado para la asignatura de Cloud Computing.

## Descripción

Este proyecto implementa un sistema de gestión documental empresarial usando servicios de AWS. La idea es simular cómo una empresa podría gestionar sus archivos de forma segura y organizada en la nube, con diferentes niveles de acceso según el departamento.

El sistema permite subir, descargar y gestionar archivos en Amazon S3, con control de acceso basado en roles y seguimiento completo de actividad.

## Características principales

- **Autenticación segura** con Amazon Cognito
- **Control de acceso granular** - Cada usuario solo puede hacer lo que su rol permite
- **Tres niveles de seguridad** - Documentos públicos, proyectos internos y recursos humanos
- **Auditoría completa** - Todos los accesos y modificaciones quedan registrados
- **Búsqueda avanzada** - Encuentra archivos rápidamente con OpenSearch
- **Versionado automático** - Se guardan versiones anteriores de los archivos

## Roles de usuario

El sistema tiene 5 tipos de usuarios diferentes:

| Rol | Permisos |
|-----|----------|
| **Solo Lectura** | Puede ver la lista de archivos y sus propiedades, pero no descargar el contenido |
| **Solo Carga** | Puede subir archivos nuevos, pero no ver qué hay en el sistema |
| **Solo Descarga** | Puede ver y descargar archivos, pero no modificarlos |
| **Lectura y Escritura** | Puede ver, descargar, subir y eliminar archivos |
| **Admin** | Acceso completo + panel de administración con logs |

## Arquitectura

```
┌─────────────┐
│  Usuario    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Amazon Cognito  │  ◄── Autenticación
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Roles  │  ◄── Control de acceso
    │  IAM   │
    └────┬───┘
         │
         ▼
┌─────────────────┐
│   Amazon S3     │  ◄── Almacenamiento
│  - Pública      │
│  - Proyectos    │
│  - RRHH         │
└────────┬────────┘
         │
         ▼
    ┌───────────┐
    │CloudTrail │  ◄── Auditoría
    └─────┬─────┘
          │
          ▼
    ┌────────────┐
    │ OpenSearch │  ◄── Búsqueda
    └────────────┘
```

## Tecnologías utilizadas

**Cloud:**
- Amazon S3 (almacenamiento)
- Amazon Cognito (autenticación)
- AWS IAM (permisos)
- CloudTrail (logs)
- OpenSearch (búsqueda)
- Lambda (procesamiento)

**Desarrollo:**
- Python 3.x
- Reflex (framework web)
- Boto3 (SDK de AWS)

## Configuración del proyecto

### Requisitos previos

- Python 3.8 o superior
- Cuenta de AWS con acceso a consola
- Git
- AWS CLI configurado

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ayalasofia0-ops/ESIT-Cloud-SN-8.git
cd ESIT-Cloud-SN-8
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales de AWS
```

5. Generar archivos de configuración:
```bash
python generate_configs.py
```

## Configuración de AWS

El proyecto incluye un script que genera automáticamente todas las configuraciones necesarias para AWS. Solo necesitas:

1. Tener una cuenta de AWS activa
2. Configurar AWS CLI con tus credenciales
3. Editar el archivo `.env` con tus IDs y credenciales
4. Ejecutar `python generate_configs.py`

Los archivos generados se guardan en `aws-config/` y están listos para aplicarse con AWS CLI.

### Aplicar configuraciones

```bash
# Ejemplo para crear buckets
aws s3api create-bucket --bucket cndd-publica --region us-east-2

# Aplicar políticas
aws iam create-policy --policy-name CNDD-Admin --policy-document file://aws-config/policies/policy-admin.json

# Y así sucesivamente...
```

Consulta la documentación en `docs/SETUP.md` para instrucciones detalladas.

## Medidas de seguridad implementadas

- ✅ Cifrado en tránsito (HTTPS obligatorio)
- ✅ Cifrado en reposo (AES-256)
- ✅ Versionado de objetos (histórico de cambios)
- ✅ Lifecycle policies (archivado automático)
- ✅ Logging completo de accesos
- ✅ Principio de mínimo privilegio
- ✅ Autenticación multi-factor (opcional)
- ✅ Políticas de bucket restrictivas

## Estructura del proyecto

```
.
├── aws-config/              # Configuraciones de AWS
│   ├── policies/           # Políticas IAM
│   ├── lifecycle/          # Reglas de ciclo de vida
│   ├── logging/            # Configuración de logs
│   ├── cognito/            # Configuración de Cognito
│   ├── opensearch/         # Configuración de OpenSearch
│   ├── cloudtrail/         # Configuración de CloudTrail
│   └── lambda/             # Funciones Lambda
├── proyecto-s3-cndd/       # Aplicación web
│   ├── config/             # Configuración de la app
│   ├── services/           # Lógica de negocio
│   ├── components/         # Componentes UI
│   └── pages/              # Páginas de la app
├── scripts/                # Scripts de utilidad
├── docs/                   # Documentación
├── .env.example           # Plantilla de variables de entorno
├── generate_configs.py    # Generador de configuraciones
└── README.md              # Este archivo
```

## Uso

### Iniciar la aplicación

```bash
cd proyecto-s3-cndd
reflex run
```

La aplicación estará disponible en `http://localhost:3000`

### Probar roles

Puedes usar el script de pruebas para verificar que cada rol funciona correctamente:

```bash
python scripts/test_roles_s3.py
```

Esto genera un reporte HTML mostrando qué operaciones puede realizar cada rol.

## Costos estimados

Para un uso de desarrollo/demostración:
- S3: ~$0.50/mes (primeros 5GB gratis)
- Cognito: Gratis (hasta 50,000 usuarios)
- CloudTrail: ~$2/mes
- OpenSearch: ~$15/mes (instancia t3.small)

**Total aproximado: $17-20/mes**

Se recomienda apagar OpenSearch cuando no se use para reducir costos.

## Problemas conocidos

- OpenSearch tarda ~15 minutos en iniciar la primera vez
- Los logs de CloudTrail pueden tardar hasta 15 minutos en aparecer
- Cognito requiere verificación de email (revisar spam)

## Próximas mejoras

- [ ] Compartir archivos entre usuarios
- [ ] Notificaciones por email
- [ ] Vista previa de archivos
- [ ] App móvil
- [ ] Integración con Office 365

## Autor

**Luis Eduardo Ayala Rayas**  
Estudiante de Ingeniería en Sistemas  
ESIT - Estancia Profesional  
Semestre: 03-25

## Agradecimientos

Gracias al profesor y a mis compañeros por el apoyo durante el desarrollo de este proyecto.

## Licencia

Este proyecto es de código abierto para fines educativos.

---

**Nota:** Este proyecto fue desarrollado con fines académicos. No se recomienda usar en producción sin una revisión exhaustiva de seguridad.
