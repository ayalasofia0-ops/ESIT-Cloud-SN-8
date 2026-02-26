# Matriz de Pruebas de Seguridad

**Fecha:** 24 de Febrero de 2026  
**Proyecto:** CNDD Project  
**Objetivo:** Verificar medidas de seguridad implementadas

---

## Resultados de Pruebas

| # | Medida de Seguridad | Implementado | Verificado | Estado | Evidencia |
|---|---------------------|--------------|------------|--------|-----------|
| 1 | Autenticación con Cognito | ✅ Sí | ✅ Sí | ✅ PASS | Tokens JWT válidos |
| 2 | Cifrado en tránsito (HTTPS) | ✅ Sí | ✅ Sí | ✅ PASS | HTTPS en URLs pre-firmadas |
| 3 | Cifrado en reposo S3 (AES-256) | ✅ Sí | ✅ Sí | ✅ PASS | Buckets con cifrado SSE-S3 |
| 4 | Versionado de objetos S3 | ✅ Sí | ✅ Sí | ✅ PASS | Versiones anteriores guardadas |
| 5 | Lifecycle policies | ✅ Sí | ✅ Sí | ✅ PASS | Archivos antiguos → Glacier |
| 6 | Políticas IAM mínimo privilegio | ✅ Sí | ✅ Sí | ✅ PASS | Cada rol tiene solo lo necesario |
| 7 | URLs pre-firmadas con expiración | ✅ Sí | ✅ Sí | ✅ PASS | Expiran en 5 minutos |
| 8 | Logout invalida tokens | ✅ Sí | ✅ Sí | ✅ PASS | global_sign_out en Cognito |
| 9 | Protección de rutas | ✅ Sí | ✅ Sí | ✅ PASS | on_mount verifica autenticación |
| 10 | Auditoría con CloudTrail | ✅ Sí | ✅ Sí | ✅ PASS | 13,313 eventos registrados |
| 11 | Logs en OpenSearch | ✅ Sí | ✅ Sí | ✅ PASS | Búsqueda funcional |
| 12 | Validación de contraseñas | ✅ Sí | ✅ Sí | ✅ PASS | Requiere mayúsculas, números |
| 13 | Sin SQL Injection | ✅ Sí | ✅ Sí | ✅ PASS | No hay SQL directo (usa boto3) |
| 14 | Sin XSS | ✅ Sí | ✅ Sí | ✅ PASS | Reflex sanitiza automáticamente |
| 15 | Separación de datos por bucket | ✅ Sí | ✅ Sí | ✅ PASS | 4 buckets independientes |

**Resultado:** 15/15 (100%)

---

## Pruebas de Penetración Básicas

| # | Intento de Ataque | Resultado | Estado |
|---|-------------------|-----------|--------|
| 1 | Acceso sin autenticación | Redirige a /login | ✅ BLOQUEADO |
| 2 | Token JWT manipulado | Rechaza token inválido | ✅ BLOQUEADO |
| 3 | Fuerza bruta de contraseña | Cognito bloquea después de intentos fallidos | ✅ BLOQUEADO |
| 4 | Acceso directo a bucket S3 | Política de bucket rechaza | ✅ BLOQUEADO |
| 5 | Subir archivo malicioso | S3 acepta cualquier tipo (solo almacena) | ⚠️ NOTA* |
| 6 | URL pre-firmada después de expirar | AWS rechaza (403 Forbidden) | ✅ BLOQUEADO |
| 7 | Usuario sin grupo intenta login | Mensaje "sin grupo asignado" | ✅ BLOQUEADO |
| 8 | Role escalation (usuario normal → admin) | IAM rechaza operaciones no permitidas | ✅ BLOQUEADO |

*Nota: S3 es agnóstico al tipo de archivo. La validación de tipo debe hacerse en la aplicación si se requiere.

---

## Compliance con Mejores Prácticas AWS

| Práctica | Implementado | Detalles |
|----------|--------------|----------|
| Principle of Least Privilege | ✅ | Cada rol IAM tiene solo lo necesario |
| Defense in Depth | ✅ | Múltiples capas: Cognito + IAM + S3 policies |
| Enable Logging | ✅ | CloudTrail + S3 access logs |
| Encrypt Data | ✅ | HTTPS + AES-256 |
| Regular Backups | ✅ | Versionado de S3 |
| Monitor and Alert | ✅ | OpenSearch para análisis |
| Use IAM Roles | ✅ | Roles en lugar de credenciales hardcoded |
| MFA (opcional) | ⚠️ | Disponible en Cognito pero no forzado |

---

## Recomendaciones Adicionales

Para producción se recomienda:

1. ⚠️ Habilitar MFA obligatorio en Cognito
2. ⚠️ Agregar validación de tipo de archivo en uploads
3. ⚠️ Implementar rate limiting en API
4. ⚠️ Agregar WAF (Web Application Firewall)
5. ⚠️ Escaneo de virus en archivos subidos
6. ⚠️ Alertas automáticas por OpenSearch

---

**Conclusión:** El proyecto cumple con estándares de seguridad para entorno académico/desarrollo. Para producción requiere endurecimiento adicional.