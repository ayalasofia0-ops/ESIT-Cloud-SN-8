# Script para crear usuarios de prueba en Cognito
# Ejecutar en PowerShell

# IMPORTANTE: Reemplaza con tu UserPoolId real
$USER_POOL_ID = "TU_USER_POOL_ID_AQUI"  # Ejemplo: us-east-2_Abc123XYZ
$REGION = "us-east-2"
$PASSWORD = "Test123!"

# Usuario 1: Solo Lectura
Write-Host "Creando usuario: Solo Lectura..." -ForegroundColor Yellow
aws cognito-idp admin-create-user `
  --user-pool-id $USER_POOL_ID `
  --username "solo.lectura@test.com" `
  --user-attributes Name=email,Value=solo.lectura@test.com Name=name,Value="Usuario Lectura" Name=email_verified,Value=true `
  --message-action SUPPRESS `
  --region $REGION

aws cognito-idp admin-set-user-password `
  --user-pool-id $USER_POOL_ID `
  --username "solo.lectura@test.com" `
  --password $PASSWORD `
  --permanent `
  --region $REGION

aws cognito-idp admin-add-user-to-group `
  --user-pool-id $USER_POOL_ID `
  --username "solo.lectura@test.com" `
  --group-name solo-lectura `
  --region $REGION

Write-Host "✓ Usuario Solo Lectura creado" -ForegroundColor Green

# Usuario 2: Solo Carga
Write-Host "`nCreando usuario: Solo Carga..." -ForegroundColor Yellow
aws cognito-idp admin-create-user `
  --user-pool-id $USER_POOL_ID `
  --username "solo.carga@test.com" `
  --user-attributes Name=email,Value=solo.carga@test.com Name=name,Value="Usuario Carga" Name=email_verified,Value=true `
  --message-action SUPPRESS `
  --region $REGION

aws cognito-idp admin-set-user-password `
  --user-pool-id $USER_POOL_ID `
  --username "solo.carga@test.com" `
  --password $PASSWORD `
  --permanent `
  --region $REGION

aws cognito-idp admin-add-user-to-group `
  --user-pool-id $USER_POOL_ID `
  --username "solo.carga@test.com" `
  --group-name solo-carga `
  --region $REGION

Write-Host "✓ Usuario Solo Carga creado" -ForegroundColor Green

# Usuario 3: Solo Descarga
Write-Host "`nCreando usuario: Solo Descarga..." -ForegroundColor Yellow
aws cognito-idp admin-create-user `
  --user-pool-id $USER_POOL_ID `
  --username "solo.descarga@test.com" `
  --user-attributes Name=email,Value=solo.descarga@test.com Name=name,Value="Usuario Descarga" Name=email_verified,Value=true `
  --message-action SUPPRESS `
  --region $REGION

aws cognito-idp admin-set-user-password `
  --user-pool-id $USER_POOL_ID `
  --username "solo.descarga@test.com" `
  --password $PASSWORD `
  --permanent `
  --region $REGION

aws cognito-idp admin-add-user-to-group `
  --user-pool-id $USER_POOL_ID `
  --username "solo.descarga@test.com" `
  --group-name solo-descarga `
  --region $REGION

Write-Host "✓ Usuario Solo Descarga creado" -ForegroundColor Green

# Usuario 4: Lectura y Escritura
Write-Host "`nCreando usuario: Lectura y Escritura..." -ForegroundColor Yellow
aws cognito-idp admin-create-user `
  --user-pool-id $USER_POOL_ID `
  --username "lec.escritura@test.com" `
  --user-attributes Name=email,Value=lec.escritura@test.com Name=name,Value="Usuario Completo" Name=email_verified,Value=true `
  --message-action SUPPRESS `
  --region $REGION

aws cognito-idp admin-set-user-password `
  --user-pool-id $USER_POOL_ID `
  --username "lec.escritura@test.com" `
  --password $PASSWORD `
  --permanent `
  --region $REGION

aws cognito-idp admin-add-user-to-group `
  --user-pool-id $USER_POOL_ID `
  --username "lec.escritura@test.com" `
  --group-name lectura-escritura `
  --region $REGION

Write-Host "✓ Usuario Lectura/Escritura creado" -ForegroundColor Green

# Usuario 5: Admin
Write-Host "`nCreando usuario: Admin..." -ForegroundColor Yellow
aws cognito-idp admin-create-user `
  --user-pool-id $USER_POOL_ID `
  --username "admin@test.com" `
  --user-attributes Name=email,Value=admin@test.com Name=name,Value="Administrador" Name=email_verified,Value=true `
  --message-action SUPPRESS `
  --region $REGION

aws cognito-idp admin-set-user-password `
  --user-pool-id $USER_POOL_ID `
  --username "admin@test.com" `
  --password $PASSWORD `
  --permanent `
  --region $REGION

aws cognito-idp admin-add-user-to-group `
  --user-pool-id $USER_POOL_ID `
  --username "admin@test.com" `
  --group-name admin `
  --region $REGION

Write-Host "✓ Usuario Admin creado" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ TODOS LOS USUARIOS CREADOS" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nCredenciales de acceso:" -ForegroundColor White
Write-Host "Email                    | Contraseña | Rol" -ForegroundColor White
Write-Host "-------------------------|------------|--------------------" -ForegroundColor White
Write-Host "solo.lectura@test.com    | $PASSWORD  | Solo Lectura" -ForegroundColor White
Write-Host "solo.carga@test.com      | $PASSWORD  | Solo Carga" -ForegroundColor White
Write-Host "solo.descarga@test.com   | $PASSWORD  | Solo Descarga" -ForegroundColor White
Write-Host "lec.escritura@test.com   | $PASSWORD  | Lectura/Escritura" -ForegroundColor White
Write-Host "admin@test.com           | $PASSWORD  | Admin" -ForegroundColor White
