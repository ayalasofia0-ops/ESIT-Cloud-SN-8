# Guía de Capturas de Evidencia - Sistema CNDD Storage

## Instrucciones Generales

### Formato de Capturas
- **Formato**: PNG (mejor calidad)
- **Resolución**: 1920x1080 o mayor
- **Herramienta**: Windows Snipping Tool (Win + Shift + S)
- **Ubicación**: `C:\Users\Luise\Documents\Portfolio\CNDD\ESIT-Cloud-SN-8\docs\evidencias\`

### Nomenclatura
Seguir exactamente los nombres definidos en TESTING_MATRIX.md:
- Ejemplo: `Cap_01_listar_exito.png`
- No usar espacios ni tildes
- Numeración con ceros a la izquierda (01, 02, 03...)

---

## CATEGORÍA 1: Permisos por Rol (21 capturas)

### Rol: Solo Lectura (5 capturas)

#### Cap_01_listar_exito.png
**Qué mostrar**: Terminal o app mostrando lista de archivos
**Comando**:
```bash
aws s3 ls s3://cndd-publica/ --profile usuario-solo-lectura
```
**Debe mostrar**: Lista de archivos sin errores

---

#### Cap_02_metadata_exito.png
**Qué mostrar**: Metadata de un archivo (tamaño, fecha, etc.)
**Comando**:
```bash
aws s3api head-object --bucket cndd-publica --key archivo.txt --profile usuario-solo-lectura
```
**Debe mostrar**: JSON con metadata del archivo

---

#### Cap_03_descarga_denegada.png
**Qué mostrar**: Error de acceso denegado al intentar descargar
**Comando**:
```bash
aws s3 cp s3://cndd-publica/archivo.txt . --profile usuario-solo-lectura
```
**Debe mostrar**: Error 403 Access Denied

---

#### Cap_04_carga_denegada.png
**Qué mostrar**: Error al intentar subir archivo
**Comando**:
```bash
echo "test" > test.txt
aws s3 cp test.txt s3://cndd-publica/ --profile usuario-solo-lectura
```
**Debe mostrar**: Error 403 Access Denied

---

#### Cap_05_eliminar_denegada.png
**Qué mostrar**: Error al intentar eliminar
**Comando**:
```bash
aws s3 rm s3://cndd-publica/archivo.txt --profile usuario-solo-lectura
```
**Debe mostrar**: Error 403 Access Denied

---

### Rol: Solo Carga (4 capturas)

#### Cap_06_listar_denegado.png
**Qué mostrar**: Error al intentar listar archivos
**Comando**:
```bash
aws s3 ls s3://cndd-proyectos/ --profile Us-carga
```
**Debe mostrar**: Error 403 o lista vacía

---

#### Cap_07_carga_exito.png
**Qué mostrar**: Carga exitosa de archivo
**Comando**:
```bash
echo "archivo de prueba" > carga-test.txt
aws s3 cp carga-test.txt s3://cndd-proyectos/ --profile Us-carga
```
**Debe mostrar**: Mensaje "upload: ./carga-test.txt to s3://cndd-proyectos/carga-test.txt"

---

#### Cap_08_descarga_denegada.png
**Qué mostrar**: Error al descargar
**Comando**:
```bash
aws s3 cp s3://cndd-proyectos/archivo.txt . --profile Us-carga
```
**Debe mostrar**: Error 403 Access Denied

---

#### Cap_09_eliminar_denegada.png
**Qué mostrar**: Error al eliminar
**Comando**:
```bash
aws s3 rm s3://cndd-proyectos/archivo.txt --profile Us-carga
```
**Debe mostrar**: Error 403 Access Denied

---

### Rol: Solo Descarga (4 capturas)

#### Cap_10_listar_exito.png
**Qué mostrar**: Lista de archivos exitosa
**Comando**:
```bash
aws s3 ls s3://cndd-recursoshumanos/ --profile Us-Descarga
```
**Debe mostrar**: Lista de archivos

---

#### Cap_11_descarga_exito.png
**Qué mostrar**: Descarga exitosa
**Comando**:
```bash
aws s3 cp s3://cndd-recursoshumanos/archivo.txt . --profile Us-Descarga
```
**Debe mostrar**: "download: s3://cndd-recursoshumanos/archivo.txt to ./archivo.txt"

---

#### Cap_12_carga_denegada.png
**Qué mostrar**: Error al subir
**Comando**:
```bash
echo "test" > test.txt
aws s3 cp test.txt s3://cndd-recursoshumanos/ --profile Us-Descarga
```
**Debe mostrar**: Error 403 Access Denied

---

#### Cap_13_eliminar_denegada.png
**Qué mostrar**: Error al eliminar
**Comando**:
```bash
aws s3 rm s3://cndd-recursoshumanos/archivo.txt --profile Us-Descarga
```
**Debe mostrar**: Error 403 Access Denied

---

### Rol: Lectura/Escritura (4 capturas)

#### Cap_14_listar_exito.png
**Comando**:
```bash
aws s3 ls s3://cndd-publica/ --profile Us-LecturaEscritura
```

#### Cap_15_carga_exito.png
**Comando**:
```bash
echo "lectura-escritura test" > lec-esc.txt
aws s3 cp lec-esc.txt s3://cndd-publica/ --profile Us-LecturaEscritura
```

#### Cap_16_descarga_exito.png
**Comando**:
```bash
aws s3 cp s3://cndd-publica/lec-esc.txt . --profile Us-LecturaEscritura
```

#### Cap_17_eliminar_exito.png
**Comando**:
```bash
aws s3 rm s3://cndd-publica/lec-esc.txt --profile Us-LecturaEscritura
```

---

### Rol: Admin (4 capturas)

#### Cap_18_admin_listar.png
**Qué mostrar**: Admin puede listar todos los buckets
**Comando**:
```bash
aws s3 ls --profile Us-Admin
```
**Debe mostrar**: Los 5 buckets

---

#### Cap_19_admin_completo.png
**Qué mostrar**: Operación completa exitosa
**Comando**:
```bash
echo "admin test" > admin.txt
aws s3 cp admin.txt s3://cndd-recursoshumanos/ --profile Us-Admin
aws s3 ls s3://cndd-recursoshumanos/ --profile Us-Admin
aws s3 rm s3://cndd-recursoshumanos/admin.txt --profile Us-Admin
```
**Debe mostrar**: Todas las operaciones exitosas

---

#### Cap_20_admin_logs.png
**Qué mostrar**: OpenSearch mostrando logs
**Dónde**: OpenSearch Dashboards → Discover
**Debe mostrar**: Eventos de CloudTrail indexados

---

#### Cap_21_admin_dashboard.png
**Qué mostrar**: Dashboard completo
**Dónde**: OpenSearch Dashboards → Dashboard → CNDD - Panel de Administración
**Debe mostrar**: Las 4 visualizaciones

---

## CATEGORÍA 2: Seguridad (11 capturas)

#### Cap_22_cifrado_reposo.png
**Qué mostrar**: Configuración de cifrado
**Dónde**: AWS Console → S3 → cndd-publica → Properties → Default encryption
**Debe mostrar**: Server-side encryption: AES-256

---

#### Cap_23_https_obligatorio.png
**Qué mostrar**: Bucket policy requiriendo HTTPS
**Dónde**: AWS Console → S3 → cndd-publica → Permissions → Bucket policy
**Debe mostrar**: Condición `"aws:SecureTransport": "false"` con Effect: Deny

---

#### Cap_24_versionado_activo.png
**Qué mostrar**: Versionado habilitado
**Dónde**: AWS Console → S3 → cndd-publica → Properties → Bucket Versioning
**Debe mostrar**: Bucket Versioning: Enabled

---

#### Cap_25_delete_marker.png
**Qué mostrar**: Delete marker después de eliminar
**Comando**:
```bash
# Subir archivo
echo "version test" > version.txt
aws s3 cp version.txt s3://cndd-publica/

# Eliminar
aws s3 rm s3://cndd-publica/version.txt

# Ver versiones
aws s3api list-object-versions --bucket cndd-publica --prefix version.txt
```
**Debe mostrar**: DeleteMarker: true

---

#### Cap_26_restauracion.png
**Qué mostrar**: Archivo restaurado desde versión anterior
**Comando**:
```bash
# Ver versiones
aws s3api list-object-versions --bucket cndd-publica --prefix version.txt

# Restaurar (copiar versión específica)
aws s3api copy-object --bucket cndd-publica --copy-source "cndd-publica/version.txt?versionId=VERSION_ID" --key version.txt

# Verificar
aws s3 ls s3://cndd-publica/version.txt
```
**Debe mostrar**: Archivo restaurado

---

#### Cap_27_lifecycle_ia.png
**Qué mostrar**: Lifecycle policy configurada
**Dónde**: AWS Console → S3 → cndd-publica → Management → Lifecycle rules
**Debe mostrar**: Regla con transición a Standard-IA a los 30 días

---

#### Cap_28_lifecycle_glacier.png
**Qué mostrar**: Transición a Glacier configurada
**Misma ubicación que Cap_27**
**Debe mostrar**: Transición a Glacier IR a los 90 días

---

#### Cap_29_access_logs.png
**Qué mostrar**: Logs de acceso generados
**Comando**:
```bash
aws s3 ls s3://cndd-logs/logs-publica/
```
**Debe mostrar**: Archivos de log

---

#### Cap_30_cloudtrail_events.png
**Qué mostrar**: Eventos de CloudTrail
**Comando**:
```bash
aws cloudtrail lookup-events --max-results 5 --region us-east-2
```
**Debe mostrar**: Lista de eventos recientes

---

#### Cap_31_no_auth_bloqueado.png
**Qué mostrar**: Acceso sin autenticación bloqueado
**Comando**:
```bash
# Sin perfil/credenciales
curl https://cndd-publica.s3.us-east-2.amazonaws.com/
```
**Debe mostrar**: Error Access Denied

---

#### Cap_32_rol_incorrecto.png
**Qué mostrar**: Rol IAM sin permisos bloqueado
**Crear usuario de prueba sin políticas y mostrar error de acceso**

---

## CATEGORÍA 3: Integración (7 capturas)

#### Cap_33_cognito_integration.png
**Qué mostrar**: User Pool y Identity Pool conectados
**Dónde**: AWS Console → Cognito → User Pool → App integration
**Debe mostrar**: App client configurado

---

#### Cap_34_role_mapping.png
**Qué mostrar**: Grupos mapeados a roles
**Dónde**: AWS Console → Cognito → User Pool → Groups
**Debe mostrar**: Los 5 grupos con sus roles IAM

---

#### Cap_35_s3_cloudtrail.png
**Qué mostrar**: CloudTrail capturando eventos S3
**Dónde**: AWS Console → CloudTrail → Event history
**Debe mostrar**: Eventos de tipo PutObject, GetObject

---

#### Cap_36_cloudtrail_s3.png
**Qué mostrar**: Logs guardados en bucket
**Comando**:
```bash
aws s3 ls s3://cndd-cloudtrail-logs/AWSLogs/430374710014/CloudTrail/us-east-2/ --recursive
```
**Debe mostrar**: Archivos .json.gz

---

#### Cap_37_s3_lambda_trigger.png
**Qué mostrar**: Configuración de trigger S3 → Lambda
**Dónde**: AWS Console → Lambda → CloudTrail-To-OpenSearch → Configuration → Triggers
**Debe mostrar**: Trigger S3: cndd-cloudtrail-logs

---

#### Cap_38_lambda_opensearch.png
**Qué mostrar**: Logs de Lambda exitosos
**Dónde**: AWS Console → Lambda → Monitor → Logs
**Debe mostrar**: "✓ Procesados X eventos"

---

#### Cap_39_opensearch_dashboard.png
**Qué mostrar**: Dashboard con datos actualizados
**Dónde**: OpenSearch Dashboards → Dashboard
**Debe mostrar**: Visualizaciones con datos

---

## CATEGORÍA 4: Manejo de Errores (7 capturas)

#### Cap_40_login_failed.png
**Qué mostrar**: Login fallido en Cognito
**Dónde**: App o AWS Console → Cognito → Users
**Simular**: Intento de login con contraseña incorrecta

---

#### Cap_41_token_expired.png
**Qué mostrar**: Error de token expirado
**Simular**: Esperar que expire sesión e intentar operación

---

#### Cap_42_file_too_large.png
**Qué mostrar**: Error al subir archivo muy grande
**Simular**: Intentar subir archivo mayor al límite

---

#### Cap_43_bucket_not_found.png
**Qué mostrar**: Error 404 bucket no existe
**Comando**:
```bash
aws s3 ls s3://bucket-inexistente/
```
**Debe mostrar**: Error NoSuchBucket

---

#### Cap_44_network_error.png
**Qué mostrar**: Error de red
**Simular**: Desconectar red e intentar operación

---

#### Cap_45_lambda_403_fixed.png
**Qué mostrar**: ANTES y DESPUÉS de solucionar error Lambda
**Dividir en 2 capturas**:
- ANTES: Error 403 en logs de Lambda
- DESPUÉS: Lambda exitosa tras mapear rol en OpenSearch

---

#### Cap_46_opensearch_down.png
**Qué mostrar**: OpenSearch inactivo (opcional)
**Solo si apagas el servicio temporalmente**

---

## CATEGORÍA 5: Rendimiento (6 capturas)

#### Cap_47_upload_10mb.png
**Qué mostrar**: Tiempo de subida
**Comando**:
```bash
# Crear archivo de 10MB
dd if=/dev/zero of=10mb.bin bs=1M count=10

# Subir con medición de tiempo
time aws s3 cp 10mb.bin s3://cndd-publica/
```
**Debe mostrar**: Tiempo real de ejecución

---

#### Cap_48_download_10mb.png
**Comando**:
```bash
time aws s3 cp s3://cndd-publica/10mb.bin .
```

---

#### Cap_49_list_100_files.png
**Qué mostrar**: Listar muchos archivos rápidamente
**Comando**:
```bash
time aws s3 ls s3://cndd-publica/
```

---

#### Cap_50_lambda_duration.png
**Qué mostrar**: Tiempo de ejecución de Lambda
**Dónde**: AWS Console → Lambda → Monitor → Recent invocations
**Debe mostrar**: Duration: X ms

---

#### Cap_51_opensearch_query.png
**Qué mostrar**: Tiempo de respuesta de query
**Dónde**: OpenSearch Dev Tools
**Ejecutar query y mostrar**: "took": X ms

---

#### Cap_52_cognito_login.png
**Qué mostrar**: Tiempo de autenticación
**Medir tiempo desde login hasta recibir token**

---

## Checklist de Capturas

### Prioridad Alta (Críticas para el proyecto)
- [ ] Cap_01 a Cap_21 (Permisos por rol)
- [ ] Cap_22 a Cap_26 (Seguridad básica)
- [ ] Cap_33 a Cap_39 (Integración)
- [ ] Cap_45 (Problema resuelto)

### Prioridad Media
- [ ] Cap_27 a Cap_32 (Seguridad avanzada)
- [ ] Cap_40 a Cap_44 (Manejo de errores)

### Prioridad Baja (Opcional)
- [ ] Cap_47 a Cap_52 (Rendimiento)
- [ ] Cap_46 (OpenSearch down)

---

## Script para Automatizar Nombres de Archivos

Crea una carpeta para evidencias:
```bash
mkdir -p docs/evidencias
cd docs/evidencias

# Crear subcarpetas por categoría
mkdir permisos seguridad integracion errores rendimiento
```

---

**Tiempo estimado para tomar todas las capturas**: 1-1.5 horas
**Herramienta recomendada**: Windows Snipping Tool (Win + Shift + S)
