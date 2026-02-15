# Problemas Encontrados y Soluciones - Sistema CNDD Storage

## Resumen Ejecutivo

Durante el desarrollo del proyecto se encontraron y resolvieron **8 problemas técnicos** principales, clasificados en 3 categorías:
- 🔴 **Críticos**: Bloquean funcionalidad (3 problemas)
- 🟡 **Medios**: Afectan rendimiento o configuración (4 problemas)
- 🟢 **Menores**: Inconsistencias o mejoras (1 problema)

**Tiempo total de debugging**: ~3 horas  
**Todos los problemas**: ✅ Resueltos

---

## PROBLEMA #1: Bucket de logs con nombre incorrecto

### Clasificación
🟡 **Severidad**: Media  
**Componente**: S3 Logging  
**Fecha**: 05 de Febrero, 2026

### Descripción
Al configurar el logging de acceso a S3, se creó el bucket con nombre `ccdn-logs` en lugar de `cndd-logs`, causando que los comandos posteriores fallen.

### Error Observado
```bash
$ aws s3api put-bucket-logging --bucket cndd-publica --bucket-logging-status file://logging-publica.json

An error occurred (NoSuchBucket) when calling the PutBucketLogging operation: The specified bucket does not exist
```

### Causa Raíz
Error tipográfico en comandos: confusión entre `ccdn` (incorrecto) y `cndd` (correcto).

### Solución Implementada
1. Verificar buckets existentes:
   ```bash
   aws s3 ls
   ```
2. Eliminar bucket incorrecto:
   ```bash
   aws s3 rb s3://ccdn-logs --force
   ```
3. Crear bucket correcto:
   ```bash
   aws s3api create-bucket --bucket cndd-logs --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2
   ```
4. Actualizar todos los archivos de configuración con el nombre correcto

### Prevención Futura
- ✅ Uso de variables de entorno centralizadas en `.env`
- ✅ Script `generate_configs.py` que previene inconsistencias
- ✅ Validación de nombres antes de ejecutar comandos

### Evidencia
- Cap_29_access_logs.png: Logs funcionando correctamente tras corrección

---

## PROBLEMA #2: Guiones vs guiones bajos en nombres de buckets

### Clasificación
🟡 **Severidad**: Media  
**Componente**: S3 Naming  
**Fecha**: 05 de Febrero, 2026

### Descripción
Inconsistencia entre convención de nombres: buckets creados con guión (`cndd-publica`) pero comandos usando guión bajo (`ccdn_publica`).

### Error Observado
```bash
$ aws s3 ls s3://ccdn_publica/
An error occurred (NoSuchBucket)
```

### Causa Raíz
Confusión en convención de nombres:
- AWS S3 requiere guiones (`-`) no guiones bajos (`_`)
- Documentación inicial usaba ambos indistintamente

### Solución Implementada
1. Estandarizar convención: **siempre usar guiones**
2. Renombrar todas las referencias en:
   - Archivos de configuración JSON
   - Scripts de testing
   - Documentación
3. Actualizar `.env` con nombres correctos

### Prevención Futura
- ✅ Documentación clara de convención de nombres
- ✅ Validación en scripts: rechazar guiones bajos
- ✅ Lint check en CI/CD (futuro)

---

## PROBLEMA #3: Políticas IAM con formato JSON incorrecto

### Clasificación
🟡 **Severidad**: Media  
**Componente**: IAM Policies  
**Fecha**: 06 de Febrero, 2026

### Descripción
Lifecycle policies rechazadas por formato JSON incorrecto en dos aspectos:
1. Campo `"Id"` debe ser `"ID"` (mayúsculas)
2. `ExpiredObjectDeleteMarker` fuera de la estructura correcta

### Error Observado
```bash
$ aws s3api put-bucket-lifecycle-configuration --bucket cndd-publica --lifecycle-configuration file://lifecycle-publica.json

An error occurred (MalformedXML) when calling the PutBucketLifecycleConfiguration operation: The XML you provided was not well-formed or did not validate against our published schema
```

### Causa Raíz
Documentación de AWS confusa sobre:
- Case sensitivity en campos JSON
- Anidación correcta de `Expiration` y sus subcampos

### Solución Implementada
**ANTES (Incorrecto)**:
```json
{
    "Rules": [{
        "Id": "LimpiezaVersiones",
        "ExpiredObjectDeleteMarker": true,
        "NoncurrentVersionExpiration": {
            "NoncurrentDays": 30
        }
    }]
}
```

**DESPUÉS (Correcto)**:
```json
{
    "Rules": [{
        "ID": "LimpiezaVersiones",
        "Expiration": {
            "ExpiredObjectDeleteMarker": true
        },
        "NoncurrentVersionExpiration": {
            "NoncurrentDays": 30
        }
    }]
}
```

### Lecciones Aprendidas
- Validar JSON con `aws s3api put-bucket-lifecycle-configuration --generate-cli-skeleton`
- Consultar ejemplos oficiales en AWS Documentation
- Usar JSON schema validator antes de aplicar

### Prevención Futura
- ✅ Templates validados incluidos en `generate_configs.py`
- ✅ Comentarios explicativos en archivos JSON

---

## PROBLEMA #4: ACL no soportadas en bucket de logs

### Clasificación
🔴 **Severidad**: Crítica  
**Componente**: S3 Access Control  
**Fecha**: 06 de Febrero, 2026

### Descripción
Al intentar configurar logging, el bucket de destino rechazaba ACLs (Access Control Lists) por configuración de ownership.

### Error Observado
```bash
$ aws s3api put-bucket-logging --bucket cndd-publica --bucket-logging-status file://logging-publica.json

An error occurred (AccessControlListNotSupported) when calling the PutBucketLogging operation: The bucket does not allow ACLs
```

### Causa Raíz
Por defecto, buckets nuevos de S3 tienen ownership controls que deshabilitan ACLs. El servicio de logging requiere ACLs para escribir en el bucket de destino.

### Solución Implementada
1. Habilitar ownership controls que permitan ACLs:
   ```bash
   aws s3api put-bucket-ownership-controls \
     --bucket cndd-logs \
     --ownership-controls Rules=[{ObjectOwnership=BucketOwnerPreferred}]
   ```
2. Aplicar configuración de logging:
   ```bash
   aws s3api put-bucket-logging \
     --bucket cndd-publica \
     --bucket-logging-status file://logging-publica.json
   ```

### Tiempo de Resolución
- Detección: 10 minutos
- Investigación: 30 minutos
- Implementación: 5 minutos
- **Total**: 45 minutos

### Prevención Futura
- ✅ Incluir ownership controls en script de creación de buckets
- ✅ Documentar requisitos de ACLs para logging

### Evidencia
- Cap_29_access_logs.png: Logs funcionando correctamente

---

## PROBLEMA #5: Política Solo Lectura permitía descargas

### Clasificación
🟢 **Severidad**: Menor (diseño)  
**Componente**: IAM Policy Logic  
**Fecha**: 07 de Febrero, 2026

### Descripción
La política "Solo Lectura" originalmente incluía `s3:GetObject`, lo que permitía descargar archivos. Esto contradecía el requisito de "solo ver metadata sin descargar contenido".

### Comportamiento Inicial
Usuario con rol "Solo Lectura" podía:
- ✅ Listar archivos
- ✅ Ver metadata
- ⚠️ **Descargar contenido** (no deseado)

### Análisis
Discusión sobre el significado de "Solo Lectura":
- **Interpretación A**: Ver metadata sin descargar
- **Interpretación B**: Descargar pero no modificar

Se decidió implementar **Interpretación A** para mayor seguridad.

### Solución Implementada
**ANTES**:
```json
{
    "Action": [
        "s3:ListBucket",
        "s3:GetObject",           ← REMOVIDO
        "s3:GetObjectAttributes",
        "s3:GetObjectMetadata"
    ]
}
```

**DESPUÉS**:
```json
{
    "Action": [
        "s3:ListBucket",
        "s3:GetObjectAttributes",
        "s3:GetObjectMetadata"
    ]
}
```

### Resultado
- ✅ Usuario puede listar archivos
- ✅ Usuario puede ver tamaño, fecha, tipo
- ❌ Usuario NO puede descargar contenido

### Evidencia
- Cap_03_descarga_denegada.png: Error 403 al intentar descargar

---

## PROBLEMA #6: CloudTrail guardando logs en bucket incorrecto

### Clasificación
🔴 **Severidad**: Crítica  
**Componente**: CloudTrail + Lambda Integration  
**Fecha**: 10 de Febrero, 2026

### Descripción
CloudTrail configurado para guardar logs en `cndd-logs` (bucket de access logs) en lugar de `cndd-cloudtrail-logs` (bucket dedicado), causando que Lambda nunca se active.

### Error Observado
- Lambda configurada con trigger en `cndd-cloudtrail-logs`
- CloudTrail escribiendo en `cndd-logs`
- Logs de CloudTrail no llegaban a OpenSearch

### Causa Raíz
Al crear el Trail inicialmente, se especificó el bucket incorrecto:
```bash
# Comando inicial (incorrecto)
aws cloudtrail create-trail --name CNDD-Trail --s3-bucket-name cndd-logs
```

### Diagnóstico
1. Verificar donde CloudTrail escribe:
   ```bash
   aws s3 ls s3://cndd-logs/ --recursive | grep CloudTrail
   # ✅ Archivos presentes aquí
   
   aws s3 ls s3://cndd-cloudtrail-logs/ --recursive
   # ❌ Vacío
   ```

2. Verificar configuración del Trail:
   ```bash
   aws cloudtrail describe-trails --trail-name-list CNDD-Trail
   # S3BucketName: "cndd-logs" ← INCORRECTO
   ```

### Solución Implementada
1. Actualizar Trail para usar bucket correcto:
   ```bash
   aws cloudtrail update-trail \
     --name CNDD-Trail \
     --s3-bucket-name cndd-cloudtrail-logs \
     --region us-east-2
   ```

2. Generar eventos de prueba para verificar:
   ```bash
   aws s3 cp test.txt s3://cndd-publica/
   aws s3 rm s3://cndd-publica/test.txt
   ```

3. Esperar 5-15 minutos y verificar:
   ```bash
   aws s3 ls s3://cndd-cloudtrail-logs/AWSLogs/430374710014/CloudTrail/us-east-2/ --recursive
   # ✅ Archivos .json.gz presentes
   ```

### Tiempo de Resolución
- Detección: 1 hora (esperando que logs lleguen)
- Investigación: 30 minutos
- Implementación: 5 minutos
- Verificación: 15 minutos
- **Total**: ~2 horas

### Prevención Futura
- ✅ Script de verificación post-configuración
- ✅ Alarma si CloudTrail no escribe en 24 horas

### Evidencia
- Cap_36_cloudtrail_s3.png: Logs en bucket correcto

---

## PROBLEMA #7: Lambda sin módulo opensearch-py

### Clasificación
🔴 **Severidad**: Crítica  
**Componente**: Lambda Deployment  
**Fecha**: 10 de Febrero, 2026

### Descripción
Función Lambda creada sin dependencias, resultando en error de importación al ejecutarse.

### Error Observado
```
[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': No module named 'opensearchpy'
```

### Causa Raíz
El paquete ZIP inicial se creó con solo el código Python, sin instalar las dependencias (`opensearch-py`, `requests-aws4auth`).

### Análisis
```bash
# ZIP inicial
$ unzip -l cloudtrail_to_opensearch.zip
Archive:  cloudtrail_to_opensearch.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     2156  2026-02-10 15:30   lambda_function.py
---------                     -------
     2156                     1 file

# Tamaño: 0.00 MB (solo código, sin dependencias)
```

### Solución Implementada
1. Crear carpeta temporal:
   ```bash
   mkdir lambda-package
   cd lambda-package
   ```

2. Instalar dependencias:
   ```bash
   pip install opensearch-py requests-aws4auth -t .
   ```

3. Copiar código:
   ```bash
   copy ..\aws-config\lambda\cloudtrail_to_opensearch.py lambda_function.py
   ```

4. Crear ZIP con dependencias:
   ```bash
   Compress-Archive -Path * -DestinationPath ..\cloudtrail_to_opensearch.zip -Force
   ```

5. Subir a S3 (archivo > 10MB):
   ```bash
   aws s3 cp cloudtrail_to_opensearch.zip s3://cndd-logs/lambda/
   ```

6. Actualizar Lambda:
   ```bash
   aws lambda update-function-code \
     --function-name CloudTrail-To-OpenSearch \
     --s3-bucket cndd-logs \
     --s3-key lambda/cloudtrail_to_opensearch.zip
   ```

### Verificación
```bash
# ZIP final
$ unzip -l cloudtrail_to_opensearch.zip | head -20
Archive:  cloudtrail_to_opensearch.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     2156  2026-02-10 18:45   lambda_function.py
    15234  2026-02-10 18:44   opensearchpy/...
    ...
---------                     -------
  8478744                     245 files

# Tamaño: 8.5 MB ✅
```

### Resultado
- ✅ Lambda ejecutándose exitosamente
- ✅ Logs indexándose en OpenSearch

### Tiempo de Resolución
- Detección: 5 minutos
- Investigación: 10 minutos
- Implementación: 15 minutos
- Verificación: 10 minutos
- **Total**: 40 minutos

### Evidencia
- Cap_38_lambda_opensearch.png: Logs de Lambda exitosos
- Cap_45_lambda_403_fixed.png: Antes y después

---

## PROBLEMA #8: Lambda sin permisos en OpenSearch (Error 403)

### Clasificación
🔴 **Severidad**: Crítica  
**Componente**: OpenSearch Security  
**Fecha**: 10 de Febrero, 2026

### Descripción
Lambda con módulos correctos pero rechazada por OpenSearch al intentar indexar documentos.

### Error Observado
```
[ERROR] AuthorizationException: AuthorizationException(403, 'security_exception', 
'no permissions for [indices:data/write/index] and User 
[name=arn:aws:iam::430374710014:role/Lambda-CloudTrail-OpenSearch, ...]')
```

### Causa Raíz
OpenSearch tiene su propio sistema de seguridad interno (Fine-Grained Access Control). Aunque el rol IAM de Lambda tiene permisos en AWS, necesita ser mapeado explícitamente dentro de OpenSearch.

### Diagrama del Problema
```
AWS IAM ✅
└── Rol: Lambda-CloudTrail-OpenSearch
    └── Política: es:ESHttpPost, es:ESHttpPut

OpenSearch Security ❌
└── No conoce el rol de Lambda
    └── No permite escribir en índices
```

### Solución Implementada
1. Acceder a OpenSearch Dashboards:
   - URL: `https://ENDPOINT/_dashboards`
   - Login: admin / Admin123!

2. Ir a Security → Roles:
   - Click en `all_access`
   - Tab "Mapped users"
   - Click "Manage mapping"

3. Agregar Backend Role:
   ```
   arn:aws:iam::430374710014:role/Lambda-CloudTrail-OpenSearch
   ```

4. Click "Map"

### Verificación
1. Generar evento nuevo:
   ```bash
   aws s3 cp test.txt s3://cndd-publica/
   aws s3 rm s3://cndd-publica/test.txt
   ```

2. Esperar 5-10 minutos

3. Verificar logs de Lambda:
   ```bash
   aws logs get-log-events --log-group-name /aws/lambda/CloudTrail-To-OpenSearch ...
   # ✅ No más errores 403
   # ✅ "Procesados X eventos exitosamente"
   ```

4. Verificar en OpenSearch:
   ```
   GET _cat/indices?v
   # ✅ cloudtrail-logs con documentos
   ```

### Tiempo de Resolución
- Detección: 10 minutos
- Investigación: 45 minutos (entender seguridad de OpenSearch)
- Implementación: 5 minutos
- Verificación: 15 minutos
- **Total**: ~1.5 horas

### Lecciones Aprendidas
- OpenSearch tiene dos capas de seguridad: IAM + interna
- Siempre mapear roles de servicios AWS en OpenSearch
- Documentar este paso crítico para futuros deployments

### Evidencia
- Cap_45_lambda_403_fixed.png: Error y solución

---

## Resumen de Problemas

| # | Problema | Severidad | Tiempo Resolución | Estado |
|---|----------|-----------|------------------|--------|
| 1 | Bucket nombre incorrecto | 🟡 Media | 30 min | ✅ Resuelto |
| 2 | Guiones vs guiones bajos | 🟡 Media | 20 min | ✅ Resuelto |
| 3 | JSON policies malformado | 🟡 Media | 45 min | ✅ Resuelto |
| 4 | ACL no soportadas | 🔴 Crítica | 45 min | ✅ Resuelto |
| 5 | Solo Lectura con GetObject | 🟢 Menor | 15 min | ✅ Resuelto |
| 6 | CloudTrail bucket incorrecto | 🔴 Crítica | 2 horas | ✅ Resuelto |
| 7 | Lambda sin dependencias | 🔴 Crítica | 40 min | ✅ Resuelto |
| 8 | Lambda sin permisos OpenSearch | 🔴 Crítica | 1.5 horas | ✅ Resuelto |

**Tiempo total de debugging**: ~6 horas  
**Problemas críticos resueltos**: 4/4 (100%)  
**Aprendizajes documentados**: 8/8 (100%)

---

## Mejoras Implementadas Post-Debugging

### 1. Automatización
- ✅ Script `generate_configs.py` previene errores de naming
- ✅ Variables centralizadas en `.env`
- ✅ Validación de JSON antes de aplicar

### 2. Documentación
- ✅ Este documento de problemas y soluciones
- ✅ Comandos de verificación incluidos
- ✅ Ejemplos de errores comunes

### 3. Prevención
- ✅ Checklist de configuración
- ✅ Scripts de verificación post-deploy
- ✅ Guías paso a paso con validaciones

---

**Fecha de última actualización**: 11 de Febrero, 2026  
**Responsable**: Luis Eduardo Ayala Rayas  
**Todos los problemas**: ✅ Resueltos y documentados
