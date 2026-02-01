"""
Script de prueba de roles IAM con S3
Prueba los 5 roles configurados y genera un reporte de resultados
"""

import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de usuarios y credenciales desde variables de entorno
USUARIOS = {
    "Solo Lectura": {
        "access_key": os.getenv("AWS_ACCESS_KEY_SOLO_LECTURA"),
        "secret_key": os.getenv("AWS_SECRET_KEY_SOLO_LECTURA"),
        "username": "usuario-solo-lectura"
    },
    "Lectura y Escritura": {
        "access_key": os.getenv("AWS_ACCESS_KEY_LECTURA_ESCRITURA"),
        "secret_key": os.getenv("AWS_SECRET_KEY_LECTURA_ESCRITURA"),
        "username": "Us-LecturaEscritura"
    },
    "Solo Carga": {
        "access_key": os.getenv("AWS_ACCESS_KEY_SOLO_CARGA"),
        "secret_key": os.getenv("AWS_SECRET_KEY_SOLO_CARGA"),
        "username": "Us-carga"
    },
    "Solo Descarga": {
        "access_key": os.getenv("AWS_ACCESS_KEY_SOLO_DESCARGA"),
        "secret_key": os.getenv("AWS_SECRET_KEY_SOLO_DESCARGA"),
        "username": "Us-Descarga"
    },
    "Admin": {
        "access_key": os.getenv("AWS_ACCESS_KEY_ADMIN"),
        "secret_key": os.getenv("AWS_SECRET_KEY_ADMIN"),
        "username": "Us-Admin"
    }
}

# Configuración de buckets
BUCKETS = ["cndd-publica", "cndd-proyectos", "cndd-recursoshumanos"]
REGION = os.getenv("AWS_REGION", "us-east-2")

# Archivo de prueba
ARCHIVO_PRUEBA = "test_archivo.txt"
CONTENIDO_PRUEBA = f"Archivo de prueba creado el {datetime.now()}"


def crear_cliente_s3(access_key, secret_key):
    """Crea un cliente S3 con las credenciales especificadas"""
    return boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=REGION
    )


def probar_listar_buckets(s3_client, rol_nombre):
    """Prueba listar buckets"""
    try:
        response = s3_client.list_buckets()
        return {
            "operacion": "Listar Buckets",
            "resultado": "✓ PERMITIDO",
            "detalles": f"Encontró {len(response['Buckets'])} buckets"
        }
    except ClientError as e:
        return {
            "operacion": "Listar Buckets",
            "resultado": "✗ DENEGADO",
            "detalles": str(e.response['Error']['Code'])
        }


def probar_listar_objetos(s3_client, bucket, rol_nombre):
    """Prueba listar objetos en un bucket"""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket)
        num_objetos = response.get('KeyCount', 0)
        return {
            "operacion": f"Listar objetos en {bucket}",
            "resultado": "✓ PERMITIDO",
            "detalles": f"Encontró {num_objetos} objetos"
        }
    except ClientError as e:
        return {
            "operacion": f"Listar objetos en {bucket}",
            "resultado": "✗ DENEGADO",
            "detalles": str(e.response['Error']['Code'])
        }


def probar_subir_archivo(s3_client, bucket, rol_nombre):
    """Prueba subir un archivo"""
    archivo_nombre = f"{rol_nombre.replace(' ', '_')}_{ARCHIVO_PRUEBA}"
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=archivo_nombre,
            Body=CONTENIDO_PRUEBA.encode('utf-8')
        )
        return {
            "operacion": f"Subir archivo a {bucket}",
            "resultado": "✓ PERMITIDO",
            "detalles": f"Archivo '{archivo_nombre}' subido exitosamente"
        }
    except ClientError as e:
        return {
            "operacion": f"Subir archivo a {bucket}",
            "resultado": "✗ DENEGADO",
            "detalles": str(e.response['Error']['Code'])
        }


def probar_descargar_archivo(s3_client, bucket, rol_nombre):
    """Prueba descargar un archivo"""
    # Intentar descargar un archivo que sabemos que existe
    archivo_nombre = f"Admin_{ARCHIVO_PRUEBA}"  # Usamos el archivo del admin para la prueba
    try:
        response = s3_client.get_object(Bucket=bucket, Key=archivo_nombre)
        contenido = response['Body'].read().decode('utf-8')
        return {
            "operacion": f"Descargar archivo de {bucket}",
            "resultado": "✓ PERMITIDO",
            "detalles": f"Archivo '{archivo_nombre}' descargado exitosamente"
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return {
                "operacion": f"Descargar archivo de {bucket}",
                "resultado": "⚠ NO HAY ARCHIVOS",
                "detalles": "No existe archivo para descargar (primero debe haber archivos)"
            }
        return {
            "operacion": f"Descargar archivo de {bucket}",
            "resultado": "✗ DENEGADO",
            "detalles": str(e.response['Error']['Code'])
        }


def probar_eliminar_archivo(s3_client, bucket, rol_nombre):
    """Prueba eliminar un archivo"""
    archivo_nombre = f"{rol_nombre.replace(' ', '_')}_{ARCHIVO_PRUEBA}"
    try:
        s3_client.delete_object(Bucket=bucket, Key=archivo_nombre)
        return {
            "operacion": f"Eliminar archivo de {bucket}",
            "resultado": "✓ PERMITIDO",
            "detalles": f"Archivo '{archivo_nombre}' eliminado exitosamente"
        }
    except ClientError as e:
        return {
            "operacion": f"Eliminar archivo de {bucket}",
            "resultado": "✗ DENEGADO",
            "detalles": str(e.response['Error']['Code'])
        }


def probar_rol(rol_nombre, credenciales):
    """Prueba todas las operaciones para un rol específico"""
    print(f"\n{'='*80}")
    print(f"PROBANDO ROL: {rol_nombre} (Usuario: {credenciales['username']})")
    print(f"{'='*80}\n")
    
    s3_client = crear_cliente_s3(credenciales['access_key'], credenciales['secret_key'])
    
    resultados = []
    
    # Probar listar buckets
    resultado = probar_listar_buckets(s3_client, rol_nombre)
    resultados.append(resultado)
    print(f"{resultado['resultado']} {resultado['operacion']}: {resultado['detalles']}")
    
    # Probar operaciones en cada bucket
    for bucket in BUCKETS:
        print(f"\n--- Bucket: {bucket} ---")
        
        # Listar objetos
        resultado = probar_listar_objetos(s3_client, bucket, rol_nombre)
        resultados.append(resultado)
        print(f"{resultado['resultado']} {resultado['operacion']}: {resultado['detalles']}")
        
        # Subir archivo
        resultado = probar_subir_archivo(s3_client, bucket, rol_nombre)
        resultados.append(resultado)
        print(f"{resultado['resultado']} {resultado['operacion']}: {resultado['detalles']}")
        
        # Descargar archivo
        resultado = probar_descargar_archivo(s3_client, bucket, rol_nombre)
        resultados.append(resultado)
        print(f"{resultado['resultado']} {resultado['operacion']}: {resultado['detalles']}")
        
        # Eliminar archivo
        resultado = probar_eliminar_archivo(s3_client, bucket, rol_nombre)
        resultados.append(resultado)
        print(f"{resultado['resultado']} {resultado['operacion']}: {resultado['detalles']}")
    
    return resultados


def generar_reporte(todos_resultados):
    """Genera un reporte HTML con todos los resultados"""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Pruebas de Roles IAM - S3</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #232F3E;
                text-align: center;
            }
            h2 {
                color: #FF9900;
                border-bottom: 2px solid #FF9900;
                padding-bottom: 5px;
            }
            .rol-section {
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #232F3E;
                color: white;
            }
            .permitido {
                color: #28a745;
                font-weight: bold;
            }
            .denegado {
                color: #dc3545;
                font-weight: bold;
            }
            .advertencia {
                color: #ffc107;
                font-weight: bold;
            }
            .fecha {
                text-align: center;
                color: #666;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>🔐 Reporte de Pruebas de Roles IAM con Amazon S3</h1>
        <div class="fecha">Generado el: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</div>
    """
    
    for rol, resultados in todos_resultados.items():
        html += f"""
        <div class="rol-section">
            <h2>{rol}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Operación</th>
                        <th>Resultado</th>
                        <th>Detalles</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for resultado in resultados:
            clase = "permitido" if "✓" in resultado['resultado'] else "denegado" if "✗" in resultado['resultado'] else "advertencia"
            html += f"""
                    <tr>
                        <td>{resultado['operacion']}</td>
                        <td class="{clase}">{resultado['resultado']}</td>
                        <td>{resultado['detalles']}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    with open('reporte_pruebas_roles.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ Reporte HTML generado: reporte_pruebas_roles.html")


def main():
    """Función principal"""
    print("="*80)
    print("INICIANDO PRUEBAS DE ROLES IAM CON AMAZON S3")
    print("="*80)
    
    todos_resultados = {}
    
    for rol_nombre, credenciales in USUARIOS.items():
        resultados = probar_rol(rol_nombre, credenciales)
        todos_resultados[rol_nombre] = resultados
    
    # Generar reporte
    generar_reporte(todos_resultados)
    
    print("\n" + "="*80)
    print("PRUEBAS COMPLETADAS")
    print("="*80)


if __name__ == "__main__":
    main()
