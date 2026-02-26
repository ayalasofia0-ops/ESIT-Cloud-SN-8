# Matriz de Pruebas de Permisos por Rol

**Fecha:** 24 de Febrero de 2026  
**Proyecto:** CNDD Project - Sistema de Gestión S3  
**Objetivo:** Verificar que cada rol tiene los permisos correctos

---

## Resultados de Pruebas

| Rol | Bucket | Listar | Ver Detalles | Descargar | Subir | Eliminar | Resultado |
|-----|--------|--------|--------------|-----------|-------|----------|-----------|
| **Admin** | cndd-publica | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ 100% |
| **Admin** | cndd-proyectos | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ 100% |
| **Admin** | cndd-rrhh | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ 100% |
| **Admin** | cndd-logs | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ 100% |
| | | | | | | | |
| **Lectura-Escritura** | cndd-publica | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ 100% |
| **Lectura-Escritura** | cndd-proyectos | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ 100% |
| **Lectura-Escritura** | cndd-rrhh | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| **Lectura-Escritura** | cndd-logs | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| | | | | | | | |
| **Solo-Lectura** | cndd-publica | ✅ PASS | ✅ PASS | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Lectura** | cndd-proyectos | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Lectura** | cndd-rrhh | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Lectura** | cndd-logs | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| | | | | | | | |
| **Solo-Carga** | cndd-publica | ✅ PASS | ✅ PASS | ❌ DENY | ✅ PASS | ❌ DENY | ✅ PASS |
| **Solo-Carga** | cndd-proyectos | ✅ PASS | ✅ PASS | ❌ DENY | ✅ PASS | ❌ DENY | ✅ PASS |
| **Solo-Carga** | cndd-rrhh | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Carga** | cndd-logs | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| | | | | | | | |
| **Solo-Descarga** | cndd-publica | ✅ PASS | ✅ PASS | ✅ PASS | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Descarga** | cndd-proyectos | ✅ PASS | ✅ PASS | ✅ PASS | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Descarga** | cndd-rrhh | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |
| **Solo-Descarga** | cndd-logs | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ❌ DENY | ✅ PASS |

---

## Resultados por Rol

| Rol | Pruebas Totales | Exitosas | Fallidas | % Éxito |
|-----|-----------------|----------|----------|---------|
| Admin | 20 | 20 | 0 | 100% |
| Lectura-Escritura | 20 | 20 | 0 | 100% |
| Solo-Lectura | 20 | 20 | 0 | 100% |
| Solo-Carga | 20 | 20 | 0 | 100% |
| Solo-Descarga | 20 | 20 | 0 | 100% |
| **TOTAL** | **100** | **100** | **0** | **100%** |

---

## Observaciones

1. ✅ Todos los permisos funcionan según lo esperado
2. ✅ Las restricciones de acceso se aplican correctamente
3. ✅ La UI muestra/oculta botones según los permisos
4. ✅ AWS rechaza operaciones no permitidas a nivel de política IAM

---

## Casos de Prueba Específicos

### Caso 1: Admin puede acceder a todo
- Usuario: admin@ejemplo.com
- Rol: admin
- Resultado: ✅ Acceso completo a los 4 buckets
- Evidencia: Puede listar, subir, descargar y eliminar en todos

### Caso 2: Solo-Lectura no puede descargar
- Usuario: lectura@test.com
- Rol: solo-lectura
- Acción: Intentar descargar archivo de cndd-publica
- Resultado: ✅ Botón de descarga NO aparece en la UI
- Evidencia: Interfaz oculta la opción

### Caso 3: Solo-Carga no puede eliminar
- Usuario: carga@test.com
- Rol: solo-carga
- Acción: Intentar eliminar archivo
- Resultado: ✅ Botón de eliminar NO aparece
- Evidencia: UI respeta permisos

---

**Conclusión:** El sistema de permisos funciona correctamente al 100%.