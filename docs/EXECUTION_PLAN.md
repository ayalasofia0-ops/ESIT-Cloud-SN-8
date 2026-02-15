# Plan Maestro de Ejecución - Documentación del Proyecto

## Tiempo Total Estimado: 2-3 horas

---

## FASE 1: Preparación (15 minutos)

### Paso 1.1: Crear estructura de carpetas
```powershell
cd C:\Users\Luise\Documents\Portfolio\CNDD\ESIT-Cloud-SN-8

# Crear carpetas de documentación
mkdir docs
mkdir docs\evidencias
mkdir docs\evidencias\permisos
mkdir docs\evidencias\seguridad
mkdir docs\evidencias\integracion
mkdir docs\evidencias\errores
mkdir docs\evidencias\rendimiento
```

### Paso 1.2: Organizar documentos descargados
Mueve los 5 documentos descargados a la carpeta `docs/`:
- ARCHITECTURE.md
- TESTING_MATRIX.md
- CAPTURE_GUIDE.md
- BEFORE_AFTER_ANALYSIS.md
- PROBLEMS_AND_SOLUTIONS.md

### Paso 1.3: Configurar perfiles AWS (si no lo has hecho)
```powershell
# Configurar perfiles para cada usuario de prueba
aws configure --profile usuario-solo-lectura
# AWS Access Key ID: [de Us-Solo-Lectura]
# AWS Secret Access Key: [de Us-Solo-Lectura]
# Region: us-east-2
# Output: json

# Repetir para:
aws configure --profile Us-carga
aws configure --profile Us-Descarga
aws configure --profile Us-LecturaEscritura
aws configure --profile Us-Admin
```

---

## FASE 2: Capturas de Permisos por Rol (45 min)

### Bloque A: Rol Solo Lectura (10 min)

#### Cap_01_listar_exito.png
```powershell
aws s3 ls s3://cndd-publica/ --profile usuario-solo-lectura
```
📸 **Captura**: Win + Shift + S → Selecciona área → Guarda como `Cap_01_listar_exito.png` en `docs\evidencias\permisos\`

---

#### Cap_02_metadata_exito.png
```powershell
# Primero sube un archivo de prueba como admin
aws s3 cp test.txt s3://cndd-publica/ --profile Us-Admin

# Luego obtén metadata como solo-lectura
aws s3api head-object --bucket cndd-publica --key test.txt --profile usuario-solo-lectura
```
📸 **Captura**: JSON con metadata del archivo

---

#### Cap_03_descarga_denegada.png
```powershell
aws s3 cp s3://cndd-publica/test.txt . --profile usuario-solo-lectura
```
📸 **Captura**: Error 403 Access Denied

---

#### Cap_04_carga_denegada.png
```powershell
echo "intento de carga" > carga-test.txt
aws s3 cp carga-test.txt s3://cndd-publica/ --profile usuario-solo-lectura
```
📸 **Captura**: Error 403 Access Denied

---

#### Cap_05_eliminar_denegada.png
```powershell
aws s3 rm s3://cndd-publica/test.txt --profile usuario-solo-lectura
```
📸 **Captura**: Error 403 Access Denied

---

### Bloque B: Rol Solo Carga (8 min)

#### Cap_06_listar_denegado.png
```powershell
aws s3 ls s3://cndd-proyectos/ --profile Us-carga
```
📸 **Captura**: Error o lista vacía

---

#### Cap_07_carga_exito.png
```powershell
echo "archivo de prueba" > archivo-carga.txt
aws s3 cp archivo-carga.txt s3://cndd-proyectos/ --profile Us-carga
```
📸 **Captura**: Mensaje de upload exitoso

---

#### Cap_08_descarga_denegada.png
```powershell
aws s3 cp s3://cndd-proyectos/archivo-carga.txt . --profile Us-carga
```
📸 **Captura**: Error 403

---

#### Cap_09_eliminar_denegada.png
```powershell
aws s3 rm s3://cndd-proyectos/archivo-carga.txt --profile Us-carga
```
📸 **Captura**: Error 403

---

### Bloque C: Rol Solo Descarga (8 min)

#### Cap_10_listar_exito.png
```powershell
aws s3 ls s3://cndd-recursoshumanos/ --profile Us-Descarga
```
📸 **Captura**: Lista de archivos

---

#### Cap_11_descarga_exito.png
```powershell
aws s3 cp s3://cndd-recursoshumanos/test.txt . --profile Us-Descarga
```
📸 **Captura**: Download exitoso

---

#### Cap_12_carga_denegada.png
```powershell
echo "test" > test-descarga.txt
aws s3 cp test-descarga.txt s3://cndd-recursoshumanos/ --profile Us-Descarga
```
📸 **Captura**: Error 403

---

#### Cap_13_eliminar_denegada.png
```powershell
aws s3 rm s3://cndd-recursoshumanos/test.txt --profile Us-Descarga
```
📸 **Captura**: Error 403

---

### Bloque D: Rol Lectura/Escritura (8 min)

#### Cap_14 a Cap_17
```powershell
# Cap_14: Listar
aws s3 ls s3://cndd-publica/ --profile Us-LecturaEscritura

# Cap_15: Subir
echo "lectura-escritura test" > lec-esc.txt
aws s3 cp lec-esc.txt s3://cndd-publica/ --profile Us-LecturaEscritura

# Cap_16: Descargar
aws s3 cp s3://cndd-publica/lec-esc.txt ./descargado.txt --profile Us-LecturaEscritura

# Cap_17: Eliminar
aws s3 rm s3://cndd-publica/lec-esc.txt --profile Us-LecturaEscritura
```
📸 **4 capturas**: Una para cada comando

---

### Bloque E: Rol Admin (11 min)

#### Cap_18: Admin lista todos los buckets
```powershell
aws s3 ls --profile Us-Admin
```
📸 **Captura**: Los 5 buckets

---

#### Cap_19: Operaciones completas
```powershell
echo "admin test" > admin.txt
aws s3 cp admin.txt s3://cndd-recursoshumanos/ --profile Us-Admin
aws s3 ls s3://cndd-recursoshumanos/ --profile Us-Admin
aws s3 rm s3://cndd-recursoshumanos/admin.txt --profile Us-Admin
```
📸 **Captura**: Todas las operaciones exitosas

---

#### Cap_20: Logs en OpenSearch
1. Abre navegador
2. Ve a: `https://TU_ENDPOINT/_dashboards`
3. Login: admin / Admin123!
4. Click en "Discover"
5. Selecciona index pattern: cloudtrail-logs
6. Filtra por eventos recientes

📸 **Captura**: Eventos visibles en Discover

---

#### Cap_21: Dashboard de admin
1. En OpenSearch Dashboards
2. Click en "Dashboard"
3. Selecciona "CNDD - Panel de Administración"
4. Espera que carguen las 4 visualizaciones

📸 **Captura**: Dashboard completo

---

## FASE 3: Capturas de Seguridad (30 min)

### Cap_22: Cifrado en reposo
1. Abre AWS Console → S3
2. Click en bucket `cndd-publica`
3. Tab "Properties"
4. Scroll a "Default encryption"

📸 **Captura**: "Server-side encryption: AES-256"

---

### Cap_23: HTTPS obligatorio
1. En S3 Console → cndd-publica
2. Tab "Permissions"
3. Scroll a "Bucket policy"

📸 **Captura**: Policy mostrando `"aws:SecureTransport": "false"` con Effect: Deny

---

### Cap_24: Versionado activo
1. S3 Console → cndd-publica
2. Tab "Properties"
3. Busca "Bucket Versioning"

📸 **Captura**: "Bucket Versioning: Enabled"

---

### Cap_25: Delete marker
```powershell
# Subir archivo
echo "version test" > version.txt
aws s3 cp version.txt s3://cndd-publica/

# Eliminar
aws s3 rm s3://cndd-publica/version.txt

# Ver versiones
aws s3api list-object-versions --bucket cndd-publica --prefix version.txt
```
📸 **Captura**: JSON mostrando DeleteMarker: true

---

### Cap_26: Restauración
```powershell
# Ver versiones (copia el VersionId del archivo, NO del delete marker)
aws s3api list-object-versions --bucket cndd-publica --prefix version.txt

# Restaurar (reemplaza VERSION_ID con el ID real)
aws s3api copy-object --bucket cndd-publica --copy-source "cndd-publica/version.txt?versionId=VERSION_ID" --key version.txt

# Verificar
aws s3 ls s3://cndd-publica/version.txt
```
📸 **Captura**: Archivo restaurado

---

### Cap_27 y Cap_28: Lifecycle policies
1. S3 Console → cndd-publica
2. Tab "Management"
3. Click en "Lifecycle rules"

📸 **2 Capturas**:
- Cap_27: Transición a Standard-IA (30 días)
- Cap_28: Transición a Glacier IR (90 días)

---

### Cap_29: Access logs
```powershell
aws s3 ls s3://cndd-logs/logs-publica/
```
📸 **Captura**: Archivos de log

---

### Cap_30: CloudTrail events
```powershell
aws cloudtrail lookup-events --max-results 5 --region us-east-2
```
📸 **Captura**: JSON con eventos recientes

---

### Cap_31: Acceso sin autenticación bloqueado
```powershell
# Intenta acceder sin credenciales
curl https://cndd-publica.s3.us-east-2.amazonaws.com/
```
📸 **Captura**: Error Access Denied

---

### Cap_32: Rol incorrecto bloqueado
(Opcional - requiere crear usuario sin políticas)

---

## FASE 4: Capturas de Integración (20 min)

### Cap_33: Cognito integration
1. AWS Console → Cognito
2. Click en User Pool "CNDD-UserPool"
3. Tab "App integration"

📸 **Captura**: App client configurado

---

### Cap_34: Role mapping
1. Cognito → User Pool → Groups
2. Muestra los 5 grupos

📸 **Captura**: Grupos con roles IAM asignados

---

### Cap_35: S3 → CloudTrail
1. AWS Console → CloudTrail
2. Event history
3. Busca eventos tipo "PutObject" o "GetObject"

📸 **Captura**: Eventos S3 en CloudTrail

---

### Cap_36: CloudTrail → S3
```powershell
aws s3 ls s3://cndd-cloudtrail-logs/AWSLogs/430374710014/CloudTrail/us-east-2/ --recursive
```
📸 **Captura**: Archivos .json.gz

---

### Cap_37: S3 → Lambda trigger
1. AWS Console → Lambda
2. Function: CloudTrail-To-OpenSearch
3. Tab "Configuration" → Triggers

📸 **Captura**: Trigger S3 configurado

---

### Cap_38: Lambda → OpenSearch
1. Lambda Console → CloudTrail-To-OpenSearch
2. Tab "Monitor" → "Logs"
3. Click en log stream más reciente

📸 **Captura**: "✓ Procesados X eventos"

---

### Cap_39: OpenSearch dashboard actualizado
1. OpenSearch Dashboards → Dashboard
2. Muestra dashboard con datos recientes

📸 **Captura**: Dashboard con visualizaciones

---

## FASE 5: Capturas de Errores (15 min)

### Cap_40 a Cap_44: Simular errores
(Opcional - requiere simular escenarios de error)

### Cap_45: Lambda 403 FIXED ⭐ IMPORTANTE
Busca en tus logs de Lambda los errores 403 anteriores y las ejecuciones exitosas posteriores.

📸 **2 Capturas**:
- ANTES: Error 403 AuthorizationException
- DESPUÉS: Ejecución exitosa

---

## FASE 6: Capturas de Rendimiento (20 min)

### Cap_47: Upload 10MB
```powershell
# Crear archivo de 10MB (Windows)
fsutil file createnew 10mb.bin 10485760

# Subir con medición de tiempo
Measure-Command { aws s3 cp 10mb.bin s3://cndd-publica/ }
```
📸 **Captura**: Tiempo de ejecución

---

### Cap_48: Download 10MB
```powershell
Measure-Command { aws s3 cp s3://cndd-publica/10mb.bin ./downloaded.bin }
```
📸 **Captura**: Tiempo de descarga

---

### Cap_49: List 100 files
```powershell
Measure-Command { aws s3 ls s3://cndd-publica/ }
```
📸 **Captura**: Tiempo de listado

---

### Cap_50: Lambda duration
1. Lambda Console → Monitor → Recent invocations
2. Click en una invocación

📸 **Captura**: Duration: X ms

---

### Cap_51: OpenSearch query time
1. OpenSearch Dev Tools
2. Ejecuta:
```json
GET cloudtrail-logs/_search
{
  "query": { "match_all": {} }
}
```
📸 **Captura**: Respuesta mostrando "took": X ms

---

### Cap_52: Cognito login time
(Requiere app web - puede omitirse)

---

## FASE 7: Commit y Push (10 min)

### Subir documentación a Git
```powershell
cd C:\Users\Luise\Documents\Portfolio\CNDD\ESIT-Cloud-SN-8

git add docs/
git commit -m "Add complete project documentation and evidence"
git push origin desarollo
```

---

## Checklist de Progreso

### Documentos Creados
- [ ] ARCHITECTURE.md
- [ ] TESTING_MATRIX.md
- [ ] CAPTURE_GUIDE.md
- [ ] BEFORE_AFTER_ANALYSIS.md
- [ ] PROBLEMS_AND_SOLUTIONS.md

### Capturas Críticas (Mínimo viable)
- [ ] Cap_01 a Cap_21 (Permisos - 21 capturas)
- [ ] Cap_20 y Cap_21 (OpenSearch funcionando)
- [ ] Cap_22, Cap_24 (Seguridad básica)
- [ ] Cap_33 a Cap_39 (Integración completa)
- [ ] Cap_45 (Problema Lambda resuelto)

### Capturas Opcionales (Extra)
- [ ] Cap_27 a Cap_32 (Seguridad avanzada)
- [ ] Cap_40 a Cap_44 (Errores simulados)
- [ ] Cap_47 a Cap_52 (Rendimiento)

---

## Tips para Ejecución Eficiente

### 1. Usa 2 pantallas
- **Pantalla 1**: Terminal ejecutando comandos
- **Pantalla 2**: Carpeta de evidencias abierta para guardar capturas

### 2. Nomenclatura estricta
- Usa exactamente los nombres especificados
- Cap_01 (con cero), no Cap_1

### 3. Calidad de capturas
- Captura solo lo necesario (no pantalla completa)
- Asegúrate que el texto sea legible
- Formato PNG

### 4. Secuencia recomendada
1. Primero todas las de terminal (Cap_01-Cap_19, Cap_29-Cap_30, etc.)
2. Luego todas las de AWS Console (Cap_22-Cap_28, Cap_33-Cap_37, etc.)
3. Luego OpenSearch (Cap_20-Cap_21, Cap_38-Cap_39, Cap_51)

### 5. Tiempo real estimado
- **Mínimo viable**: 1.5 horas (capturas críticas)
- **Completo**: 2.5-3 horas (todas las capturas)

---

**¡Éxito con la documentación!** 🚀
