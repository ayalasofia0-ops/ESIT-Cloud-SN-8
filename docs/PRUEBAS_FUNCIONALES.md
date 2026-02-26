# Matriz de Pruebas Funcionales

**Fecha:** 24 de Febrero de 2026  
**Proyecto:** CNDD Project  
**Tester:** Luis Martel

---

## Módulo 1: Autenticación

| # | Caso de Prueba | Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|---|----------------|---------|--------------------|--------------------|--------|
| 1.1 | Login exitoso con credenciales válidas | Email: admin@ejemplo.com<br>Pass: Admin123! | Redirige a /dashboard | Redirige correctamente | ✅ PASS |
| 1.2 | Login con email incorrecto | Email: noexiste@test.com<br>Pass: Admin123! | Mensaje de error | "Usuario no encontrado" | ✅ PASS |
| 1.3 | Login con contraseña incorrecta | Email: admin@ejemplo.com<br>Pass: wrongpass | Mensaje de error | "Usuario o contraseña incorrectos" | ✅ PASS |
| 1.4 | Login con campos vacíos | Email: (vacío)<br>Pass: (vacío) | Mensaje de validación | "Por favor ingresa usuario y contraseña" | ✅ PASS |
| 1.5 | Logout | Click en botón "Salir" | Cierra sesión y redirige a /login | Funciona correctamente | ✅ PASS |
| 1.6 | Protección de rutas | Acceder a /dashboard sin login | Redirige a /login | Redirige correctamente | ✅ PASS |

**Resultado del módulo:** 6/6 (100%)

---

## Módulo 2: Dashboard

| # | Caso de Prueba | Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|---|----------------|---------|--------------------|--------------------|--------|
| 2.1 | Mostrar nombre del usuario | Login exitoso | Muestra nombre completo | "¡Bienvenido, Luis Martel!" | ✅ PASS |
| 2.2 | Mostrar rol correcto | Login como admin | Muestra "Rol: admin" | Muestra correctamente | ✅ PASS |
| 2.3 | Cards según rol (admin) | Login como admin | Muestra 3 cards (Archivos, Usuarios, Logs) | Muestra 3 cards | ✅ PASS |
| 2.4 | Cards según rol (no admin) | Login como lectura-escritura | Muestra solo card de Archivos | Solo muestra Archivos | ✅ PASS |
| 2.5 | Información de permisos | Ver sección de permisos | Muestra permisos del rol actual | Información correcta | ✅ PASS |

**Resultado del módulo:** 5/5 (100%)

---

## Módulo 3: Gestión de Archivos

| # | Caso de Prueba | Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|---|----------------|---------|--------------------|--------------------|--------|
| 3.1 | Listar archivos | Seleccionar bucket cndd-publica | Muestra lista de archivos | Lista correcta con tamaños y fechas | ✅ PASS |
| 3.2 | Búsqueda de archivos | Query: "test" | Filtra archivos que contienen "test" | Filtro funciona correctamente | ✅ PASS |
| 3.3 | Subir archivo (admin) | Archivo: test.txt (1KB) | Archivo se sube correctamente | Archivo visible en lista | ✅ PASS |
| 3.4 | Descargar archivo | Click en botón descargar | Descarga automática del archivo | Archivo descargado | ✅ PASS |
| 3.5 | Eliminar archivo | Click en eliminar + confirmar | Archivo se elimina y desaparece de lista | Funciona correctamente | ✅ PASS |
| 3.6 | Cambiar de bucket | Seleccionar cndd-proyectos | Muestra archivos del nuevo bucket | Lista se actualiza | ✅ PASS |
| 3.7 | Refrescar lista | Click en botón refrescar | Recarga archivos del bucket | Lista se actualiza | ✅ PASS |
| 3.8 | Upload sin permisos | Login como solo-lectura | Botón upload NO visible | Botón oculto correctamente | ✅ PASS |

**Resultado del módulo:** 8/8 (100%)

---

## Módulo 4: Panel de Administración

| # | Caso de Prueba | Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|---|----------------|---------|--------------------|--------------------|--------|
| 4.1 | Acceso solo admin | Login como admin | Puede acceder a /admin | Acceso permitido | ✅ PASS |
| 4.2 | Restricción no-admin | Login como lectura-escritura | Redirige a /dashboard | Redirige correctamente | ✅ PASS |
| 4.3 | Crear usuario válido | Email: nuevo@test.com<br>Pass: Test123!<br>Nombre: Nuevo Usuario<br>Rol: solo-lectura | Usuario creado exitosamente | Mensaje de éxito | ✅ PASS |
| 4.4 | Crear usuario sin email | Email: (vacío)<br>Pass: Test123! | Mensaje de error | "Email y contraseña son requeridos" | ✅ PASS |
| 4.5 | Crear usuario sin contraseña | Email: test@test.com<br>Pass: (vacío) | Mensaje de error | "Email y contraseña son requeridos" | ✅ PASS |
| 4.6 | Ver logs de CloudTrail | Click en pestaña "Ver Logs" | Muestra logs en tabla | Tabla con eventos reales | ✅ PASS |
| 4.7 | Buscar logs | Query: "PutObject" | Filtra eventos de tipo PutObject | Filtro funciona | ✅ PASS |
| 4.8 | Estadísticas de logs | Ver badge de total eventos | Muestra total de eventos | Muestra número correcto | ✅ PASS |

**Resultado del módulo:** 8/8 (100%)

---

## Módulo 5: Interfaz de Usuario

| # | Caso de Prueba | Entrada | Resultado Esperado | Resultado Obtenido | Estado |
|---|----------------|---------|--------------------|--------------------|--------|
| 5.1 | Navbar en todas las páginas | Navegar entre páginas | Navbar siempre visible | Navbar persistente | ✅ PASS |
| 5.2 | Información del usuario en navbar | Login | Muestra nombre, email y rol | Información correcta | ✅ PASS |
| 5.3 | Navegación entre páginas | Click en links del navbar | Navega correctamente | Funciona | ✅ PASS |
| 5.4 | Mensajes de error | Operación fallida | Muestra mensaje en rojo | Callout rojo visible | ✅ PASS |
| 5.5 | Mensajes de éxito | Operación exitosa | Muestra mensaje en verde/azul | Callout visible | ✅ PASS |
| 5.6 | Loading indicators | Operación en proceso | Muestra spinner | Spinner visible | ✅ PASS |
| 5.7 | Confirmaciones | Eliminar archivo | Muestra diálogo de confirmación | Diálogo funciona | ✅ PASS |

**Resultado del módulo:** 7/7 (100%)

---

## Resumen General

| Módulo | Pruebas | Exitosas | Fallidas | % Éxito |
|--------|---------|----------|----------|---------|
| Autenticación | 6 | 6 | 0 | 100% |
| Dashboard | 5 | 5 | 0 | 100% |
| Gestión de Archivos | 8 | 8 | 0 | 100% |
| Panel Admin | 8 | 8 | 0 | 100% |
| Interfaz UI | 7 | 7 | 0 | 100% |
| **TOTAL** | **34** | **34** | **0** | **100%** |

---

## Conclusiones

✅ **Todas las funcionalidades probadas funcionan correctamente**  
✅ El sistema maneja errores apropiadamente  
✅ La validación de permisos funciona en todos los niveles  
✅ La interfaz es intuitiva y responsiva  

**Estado del proyecto:** APROBADO para producción académica