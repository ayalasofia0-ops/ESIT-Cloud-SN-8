#!/usr/bin/env python3
"""
Script para crear paquete de despliegue de función Lambda
"""

import os
import shutil
import zipfile
from pathlib import Path

# Configuración
LAMBDA_DIR = Path("lambda-package")
LAMBDA_CODE = Path("aws-config/lambda/cloudtrail_to_opensearch.py")
OUTPUT_ZIP = Path("cloudtrail_to_opensearch.zip")

def create_lambda_package():
    """Crea el paquete ZIP para Lambda con dependencias"""
    
    print("🚀 Creando paquete de Lambda...\n")
    
    # Limpiar directorio anterior si existe
    if LAMBDA_DIR.exists():
        shutil.rmtree(LAMBDA_DIR)
    
    LAMBDA_DIR.mkdir()
    
    # Instalar dependencias en el directorio
    print("📦 Instalando dependencias...")
    os.system(f"pip install opensearch-py requests-aws4auth -t {LAMBDA_DIR}")
    
    # Copiar código de la función
    print("\n📄 Copiando código de la función...")
    shutil.copy(LAMBDA_CODE, LAMBDA_DIR / "lambda_function.py")
    
    # Crear ZIP
    print("\n🗜️  Creando archivo ZIP...")
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(LAMBDA_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(LAMBDA_DIR)
                zipf.write(file_path, arcname)
    
    # Limpiar directorio temporal
    shutil.rmtree(LAMBDA_DIR)
    
    file_size = OUTPUT_ZIP.stat().st_size / (1024 * 1024)  # MB
    
    print(f"\n✅ Paquete creado exitosamente!")
    print(f"📦 Archivo: {OUTPUT_ZIP}")
    print(f"📊 Tamaño: {file_size:.2f} MB")
    print(f"\n💡 Ahora puedes subirlo a AWS Lambda")

if __name__ == "__main__":
    try:
        create_lambda_package()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)
