# Matriz de Pruebas - Sistema CNDD Storage

## 1. Matriz de Pruebas por Rol

| # | Rol | Operación | Bucket | Resultado Esperado | Estado | Evidencia |
|---|-----|-----------|--------|-------------------|--------|-----------|
| 1 | Solo Lectura | Listar archivos | cndd-publica | ✅ Éxito | ✅ Pass | Cap_01_listar_exito.png |
| 2 | Solo Lectura | Ver metadata | cndd-publica | ✅ Éxito | ✅ Pass | Cap_02_metadata_exito.png |
| 3 | Solo Lectura | Descargar archivo | cndd-publica | ❌ Acceso denegado | ✅ Pass | Cap_03_descarga_denegada.png |
| 4 | Solo Lectura | Subir archivo | cndd-publica | ❌ Acceso denegado | ✅ Pass | Cap_04_carga_denegada.png |
| 5 | Solo Lectura | Eliminar archivo | cndd-publica | ❌ Acceso denegado | ✅ Pass | Cap_05_eliminar_denegada.png |
| 6 | Solo Carga | Listar archivos | cndd-proyectos | ❌ Acceso denegado | ✅ Pass | Cap_06_listar_denegado.png |
| 7 | Solo Carga | Subir archivo | cndd-proyectos | ✅ Éxito | ✅ Pass | Cap_07_carga_exito.png |
| 8 | Solo Carga | Descargar archivo | cndd-proyectos | ❌ Acceso denegado | ✅ Pass | Cap_08_descarga_denegada.png |
| 9 | Solo Carga | Eliminar archivo | cndd-proyectos | ❌ Acceso denegado | ✅ Pass | Cap_09_eliminar_denegada.png |
| 10 | Solo Descarga | Listar archivos | cndd-recursoshumanos | ✅ Éxito | ✅ Pass | Cap_10_listar_exito.png |
| 11 | Solo Descarga | Descargar archivo | cndd-recursoshumanos | ✅ Éxito | ✅ Pass | Cap_11_descarga_exito.png |
| 12 | Solo Descarga | Subir archivo | cndd-recursoshumanos | ❌ Acceso denegado | ✅ Pass | Cap_12_carga_denegada.png |
| 13 | Solo Descarga | Eliminar archivo | cndd-recursoshumanos | ❌ Acceso denegado | ✅ Pass | Cap_13_eliminar_denegada.png |
| 14 | Lectura/Escritura | Listar archivos | cndd-publica | ✅ Éxito | ✅ Pass | Cap_14_listar_exito.png |
| 15 | Lectura/Escritura | Subir archivo | cndd-publica | ✅ Éxito | ✅ Pass | Cap_15_carga_exito.png |
| 16 | Lectura/Escritura | Descargar archivo | cndd-publica | ✅ Éxito | ✅ Pass | Cap_16_descarga_exito.png |
| 17 | Lectura/Escritura | Eliminar archivo | cndd-publica | ✅ Éxito | ✅ Pass | Cap_17_eliminar_exito.png |
| 18 | Admin | Listar archivos | Todos | ✅ Éxito | ✅ Pass | Cap_18_admin_listar.png |
| 19 | Admin | Todas las operaciones | Todos | ✅ Éxito | ✅ Pass | Cap_19_admin_completo.png |
| 20 | Admin | Ver logs CloudTrail | OpenSearch | ✅ Éxito | ✅ Pass | Cap_20_admin_logs.png |
| 21 | Admin | Dashboard monitoreo | OpenSearch | ✅ Éxito | ✅ Pass | Cap_21_admin_dashboard.png |

---

## 2. Matriz de Pruebas de Seguridad

| # | Categoría | Prueba | Resultado Esperado | Estado | Evidencia |
|---|-----------|--------|-------------------|--------|-----------|
| 22 | Cifrado | Verificar cifrado en reposo | ✅ AES-256 activo | ✅ Pass | Cap_22_cifrado_reposo.png |
| 23 | Cifrado | Verificar HTTPS obligatorio | ❌ HTTP bloqueado | ✅ Pass | Cap_23_https_obligatorio.png |
| 24 | Versionado | Subir archivo duplicado | ✅ Nueva versión creada | ✅ Pass | Cap_24_versionado_activo.png |
| 25 | Versionado | Eliminar archivo | ✅ Delete marker creado | ✅ Pass | Cap_25_delete_marker.png |
| 26 | Versionado | Restaurar versión anterior | ✅ Archivo restaurado | ✅ Pass | Cap_26_restauracion.png |
| 27 | Lifecycle | Archivo 30+ días | ✅ Movido a Standard-IA | ⏳ Pending | Cap_27_lifecycle_ia.png |
| 28 | Lifecycle | Archivo 90+ días | ✅ Movido a Glacier | ⏳ Pending | Cap_28_lifecycle_glacier.png |
| 29 | Logging | Verificar logs de acceso | ✅ Logs en cndd-logs | ✅ Pass | Cap_29_access_logs.png |
| 30 | CloudTrail | Verificar eventos S3 | ✅ Eventos registrados | ✅ Pass | Cap_30_cloudtrail_events.png |
| 31 | Bucket Policy | Usuario no autenticado | ❌ Acceso bloqueado | ✅ Pass | Cap_31_no_auth_bloqueado.png |
| 32 | Bucket Policy | Rol IAM incorrecto | ❌ Acceso bloqueado | ✅ Pass | Cap_32_rol_incorrecto.png |

---

## 3. Matriz de Pruebas de Integración

| # | Componente A | Componente B | Prueba | Resultado Esperado | Estado | Evidencia |
|---|--------------|--------------|--------|-------------------|--------|-----------|
| 33 | Cognito User Pool | Cognito Identity Pool | Login genera credenciales AWS | ✅ Credenciales temporales | ✅ Pass | Cap_33_cognito_integration.png |
| 34 | Identity Pool | Rol IAM | Grupo asigna rol correcto | ✅ Rol asignado según grupo | ✅ Pass | Cap_34_role_mapping.png |
| 35 | S3 | CloudTrail | Evento S3 registrado | ✅ Evento en CloudTrail | ✅ Pass | Cap_35_s3_cloudtrail.png |
| 36 | CloudTrail | S3 Bucket Logs | Log guardado correctamente | ✅ Archivo .json.gz creado | ✅ Pass | Cap_36_cloudtrail_s3.png |
| 37 | S3 Bucket Logs | Lambda | Lambda se activa con trigger | ✅ Lambda ejecutada | ✅ Pass | Cap_37_s3_lambda_trigger.png |
| 38 | Lambda | OpenSearch | Logs indexados | ✅ Documentos en índice | ✅ Pass | Cap_38_lambda_opensearch.png |
| 39 | OpenSearch | Dashboard | Visualizaciones actualizadas | ✅ Datos en tiempo real | ✅ Pass | Cap_39_opensearch_dashboard.png |

---

## 4. Matriz de Pruebas de Errores

| # | Escenario de Error | Acción | Resultado Esperado | Estado | Evidencia |
|---|-------------------|--------|-------------------|--------|-----------|
| 40 | Credenciales incorrectas | Login en Cognito | ❌ Error de autenticación | ✅ Pass | Cap_40_login_failed.png |
| 41 | Token expirado | Operación S3 | ❌ Solicitar nuevo login | ✅ Pass | Cap_41_token_expired.png |
| 42 | Archivo muy grande | Subir >5GB | ❌ Error de tamaño | ✅ Pass | Cap_42_file_too_large.png |
| 43 | Bucket no existe | Listar archivos | ❌ Error 404 | ✅ Pass | Cap_43_bucket_not_found.png |
| 44 | Red desconectada | Cualquier operación | ❌ Error de conexión | ✅ Pass | Cap_44_network_error.png |
| 45 | Lambda sin permisos | Indexar en OpenSearch | ❌ Error 403 | ✅ Fixed | Cap_45_lambda_403_fixed.png |
| 46 | OpenSearch inactivo | Ver dashboard | ❌ Error de conexión | ⏳ N/A | Cap_46_opensearch_down.png |

---

## 5. Matriz de Pruebas de Rendimiento

| # | Prueba | Métrica | Valor Esperado | Valor Obtenido | Estado | Evidencia |
|---|--------|---------|----------------|----------------|--------|-----------|
| 47 | Subir archivo 10MB | Tiempo | < 5 segundos | 3.2 segundos | ✅ Pass | Cap_47_upload_10mb.png |
| 48 | Descargar archivo 10MB | Tiempo | < 5 segundos | 2.8 segundos | ✅ Pass | Cap_48_download_10mb.png |
| 49 | Listar 100 archivos | Tiempo | < 2 segundos | 1.5 segundos | ✅ Pass | Cap_49_list_100_files.png |
| 50 | Lambda procesamiento | Tiempo | < 10 segundos | 6.3 segundos | ✅ Pass | Cap_50_lambda_duration.png |
| 51 | OpenSearch query | Tiempo | < 1 segundo | 0.4 segundos | ✅ Pass | Cap_51_opensearch_query.png |
| 52 | Login Cognito | Tiempo | < 2 segundos | 1.1 segundos | ✅ Pass | Cap_52_cognito_login.png |

---

## 6. Resumen de Resultados

### Por Categoría

| Categoría | Total Pruebas | ✅ Pass | ❌ Fail | ⏳ Pending | % Éxito |
|-----------|---------------|---------|---------|-----------|---------|
| Permisos por Rol | 21 | 21 | 0 | 0 | 100% |
| Seguridad | 11 | 9 | 0 | 2 | 81.8% |
| Integración | 7 | 7 | 0 | 0 | 100% |
| Manejo de Errores | 7 | 6 | 0 | 1 | 85.7% |
| Rendimiento | 6 | 6 | 0 | 0 | 100% |
| **TOTAL** | **52** | **49** | **0** | **3** | **94.2%** |

### Leyenda de Estados
- ✅ **Pass**: Prueba exitosa, comportamiento esperado
- ❌ **Fail**: Prueba fallida, requiere corrección
- ⏳ **Pending**: Prueba pendiente (requiere tiempo de espera)
- 🔧 **Fixed**: Error encontrado y corregido

---

## 7. Notas Importantes

### Pruebas Pendientes (⏳)
- **Cap_27 & Cap_28**: Lifecycle Policies requieren 30-90 días para verificar
- **Cap_46**: OpenSearch inactivo - Escenario no reproducible sin apagar servicio

### Problemas Encontrados y Resueltos
1. **Lambda Error 403** (Prueba #45)
   - **Problema**: Lambda sin permisos para escribir en OpenSearch
   - **Solución**: Mapear rol Lambda en OpenSearch Security
   - **Estado**: ✅ Resuelto

2. **CloudTrail en bucket incorrecto** (Prueba #35)
   - **Problema**: Logs en cndd-logs en lugar de cndd-cloudtrail-logs
   - **Solución**: Actualizar configuración del Trail
   - **Estado**: ✅ Resuelto

3. **Lambda sin dependencias** (Prueba #37)
   - **Problema**: Módulo opensearch-py no encontrado
   - **Solución**: Recrear paquete con dependencias correctas
   - **Estado**: ✅ Resuelto

---

## 8. Comandos para Reproducir Pruebas

### Pruebas de permisos (Pruebas #1-21)
```bash
# Usando el script test_roles_s3.py
python scripts/test_roles_s3.py
```

### Verificar versionado (Pruebas #24-26)
```bash
# Ver versiones de un archivo
aws s3api list-object-versions --bucket cndd-publica --prefix archivo.txt

# Restaurar versión
aws s3api copy-object --bucket cndd-publica --copy-source cndd-publica/archivo.txt?versionId=VERSION_ID --key archivo.txt
```

### Verificar logs (Pruebas #29-30)
```bash
# Access logs
aws s3 ls s3://cndd-logs/logs-publica/

# CloudTrail logs
aws s3 ls s3://cndd-cloudtrail-logs/AWSLogs/430374710014/CloudTrail/us-east-2/
```

### Verificar OpenSearch (Pruebas #38-39)
```bash
# Ver índices
GET _cat/indices?v

# Buscar eventos
GET cloudtrail-logs/_search
{
  "query": { "match_all": {} }
}
```

---

**Fecha de última actualización**: 11 de Febrero, 2026  
**Responsable**: Luis Enrique Muñoz Martel  
**Estado General del Proyecto**: 94.2% de pruebas exitosas
