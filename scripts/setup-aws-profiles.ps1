# Script para configurar perfiles AWS CLI desde variables de entorno
# Ejecutar en PowerShell desde la raiz del proyecto

# Cargar variables de .env
if (-not (Test-Path ".env")) {
    Write-Host "Error: Archivo .env no encontrado" -ForegroundColor Red
    Write-Host "Asegurate de estar en la raiz del proyecto" -ForegroundColor Yellow
    exit 1
}

Write-Host "Leyendo credenciales desde .env..." -ForegroundColor Cyan

# Leer .env y crear hashtable con las variables
$envVars = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Region por defecto
$region = $envVars["AWS_REGION"]
if (-not $region) { 
    $region = "us-east-2" 
}

Write-Host ""
Write-Host "Configurando perfiles AWS CLI..." -ForegroundColor Cyan
Write-Host "Region: $region" -ForegroundColor White
Write-Host ""

# Perfil 1: usuario-solo-lectura
$accessKey1 = $envVars["AWS_ACCESS_KEY_SOLO_LECTURA"]
$secretKey1 = $envVars["AWS_SECRET_KEY_SOLO_LECTURA"]

if ($accessKey1 -and $secretKey1) {
    Write-Host "Configurando perfil: usuario-solo-lectura..." -ForegroundColor White
    aws configure set aws_access_key_id $accessKey1 --profile usuario-solo-lectura
    aws configure set aws_secret_access_key $secretKey1 --profile usuario-solo-lectura
    aws configure set region $region --profile usuario-solo-lectura
    aws configure set output json --profile usuario-solo-lectura
    Write-Host "OK Perfil usuario-solo-lectura configurado" -ForegroundColor Green
} else {
    Write-Host "Saltando usuario-solo-lectura (credenciales no encontradas)" -ForegroundColor Yellow
}

# Perfil 2: Us-carga
$accessKey2 = $envVars["AWS_ACCESS_KEY_SOLO_CARGA"]
$secretKey2 = $envVars["AWS_SECRET_KEY_SOLO_CARGA"]

if ($accessKey2 -and $secretKey2) {
    Write-Host "Configurando perfil: Us-carga..." -ForegroundColor White
    aws configure set aws_access_key_id $accessKey2 --profile Us-carga
    aws configure set aws_secret_access_key $secretKey2 --profile Us-carga
    aws configure set region $region --profile Us-carga
    aws configure set output json --profile Us-carga
    Write-Host "OK Perfil Us-carga configurado" -ForegroundColor Green
} else {
    Write-Host "Saltando Us-carga (credenciales no encontradas)" -ForegroundColor Yellow
}

# Perfil 3: Us-Descarga
$accessKey3 = $envVars["AWS_ACCESS_KEY_SOLO_DESCARGA"]
$secretKey3 = $envVars["AWS_SECRET_KEY_SOLO_DESCARGA"]

if ($accessKey3 -and $secretKey3) {
    Write-Host "Configurando perfil: Us-Descarga..." -ForegroundColor White
    aws configure set aws_access_key_id $accessKey3 --profile Us-Descarga
    aws configure set aws_secret_access_key $secretKey3 --profile Us-Descarga
    aws configure set region $region --profile Us-Descarga
    aws configure set output json --profile Us-Descarga
    Write-Host "OK Perfil Us-Descarga configurado" -ForegroundColor Green
} else {
    Write-Host "Saltando Us-Descarga (credenciales no encontradas)" -ForegroundColor Yellow
}

# Perfil 4: Us-LecturaEscritura
$accessKey4 = $envVars["AWS_ACCESS_KEY_LECTURA_ESCRITURA"]
$secretKey4 = $envVars["AWS_SECRET_KEY_LECTURA_ESCRITURA"]

if ($accessKey4 -and $secretKey4) {
    Write-Host "Configurando perfil: Us-LecturaEscritura..." -ForegroundColor White
    aws configure set aws_access_key_id $accessKey4 --profile Us-LecturaEscritura
    aws configure set aws_secret_access_key $secretKey4 --profile Us-LecturaEscritura
    aws configure set region $region --profile Us-LecturaEscritura
    aws configure set output json --profile Us-LecturaEscritura
    Write-Host "OK Perfil Us-LecturaEscritura configurado" -ForegroundColor Green
} else {
    Write-Host "Saltando Us-LecturaEscritura (credenciales no encontradas)" -ForegroundColor Yellow
}

# Perfil 5: Us-Admin
$accessKey5 = $envVars["AWS_ACCESS_KEY_ADMIN"]
$secretKey5 = $envVars["AWS_SECRET_KEY_ADMIN"]

if ($accessKey5 -and $secretKey5) {
    Write-Host "Configurando perfil: Us-Admin..." -ForegroundColor White
    aws configure set aws_access_key_id $accessKey5 --profile Us-Admin
    aws configure set aws_secret_access_key $secretKey5 --profile Us-Admin
    aws configure set region $region --profile Us-Admin
    aws configure set output json --profile Us-Admin
    Write-Host "OK Perfil Us-Admin configurado" -ForegroundColor Green
} else {
    Write-Host "Saltando Us-Admin (credenciales no encontradas)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PERFILES CONFIGURADOS EXITOSAMENTE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Perfiles disponibles:" -ForegroundColor White
Write-Host "- usuario-solo-lectura" -ForegroundColor White
Write-Host "- Us-carga" -ForegroundColor White
Write-Host "- Us-Descarga" -ForegroundColor White
Write-Host "- Us-LecturaEscritura" -ForegroundColor White
Write-Host "- Us-Admin" -ForegroundColor White
Write-Host ""
Write-Host "Prueba de verificacion:" -ForegroundColor Yellow
Write-Host "aws s3 ls --profile usuario-solo-lectura" -ForegroundColor Gray
