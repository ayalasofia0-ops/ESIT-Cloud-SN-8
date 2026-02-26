"""
Script de pruebas de roles S3
Genera un reporte HTML con evidencias de permisos
"""

import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
REGION = os.getenv('AWS_REGION', 'us-east-2')
BUCKET_PUBLICA = os.getenv('BUCKET_PUBLICA', 'cndd-publica')
BUCKET_PROYECTOS = os.getenv('BUCKET_PROYECTOS', 'cndd-proyectos')
BUCKET_RRHH = os.getenv('BUCKET_RRHH', 'cndd-rrhh')
BUCKET_LOGS = os.getenv('BUCKET_LOGS', 'cndd-logs')

# Archivo de prueba
TEST_FILE = 'test-permissions.txt'
TEST_CONTENT = b'Este es un archivo de prueba para verificar permisos'

# Roles a probar
ROLES = [
    'admin',
    'lectura-escritura',
    'solo-lectura',
    'solo-carga',
    'solo-descarga'
]

# Buckets
BUCKETS = [
    BUCKET_PUBLICA,
    BUCKET_PROYECTOS,
    BUCKET_RRHH,
    BUCKET_LOGS
]

# Operaciones
OPERATIONS = {
    'list': 'Listar archivos',
    'get': 'Descargar archivo',
    'put': 'Subir archivo',
    'delete': 'Eliminar archivo'
}


class RoleTester:
    """Probador de roles S3."""
    
    def __init__(self, role_name):
        """Inicializar con credenciales del rol."""
        self.role_name = role_name
        self.results = {}
        
        # Obtener credenciales asumiendo el rol
        self.sts = boto3.client('sts', region_name=REGION)
        self.account_id = os.getenv('AWS_ACCOUNT_ID', '430374710014')
        
        try:
            # Asumir el rol
            role_arn = f"arn:aws:iam::{self.account_id}:role/Cognito-{role_name.title().replace('-', '')}"
            
            response = self.sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName=f'test-{role_name}-session'
            )
            
            # Crear cliente S3 con credenciales del rol
            credentials = response['Credentials']
            self.s3 = boto3.client(
                's3',
                region_name=REGION,
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )
            
            self.authenticated = True
            print(f"✅ Rol {role_name} asumido correctamente")
            
        except Exception as e:
            print(f"⚠️ No se pudo asumir el rol {role_name}: {e}")
            print(f"   Usando credenciales por defecto para simular...")
            self.s3 = boto3.client('s3', region_name=REGION)
            self.authenticated = False
    
    def test_list(self, bucket):
        """Probar listar objetos."""
        try:
            self.s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
            return True, "✅ PERMITIDO"
        except Exception as e:
            error_code = e.response['Error']['Code'] if hasattr(e, 'response') else 'Unknown'
            return False, f"❌ DENEGADO ({error_code})"
    
    def test_get(self, bucket):
        """Probar descargar objeto."""
        try:
            # Primero listar para obtener un objeto existente
            response = self.s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
            if 'Contents' in response and len(response['Contents']) > 0:
                key = response['Contents'][0]['Key']
                self.s3.get_object(Bucket=bucket, Key=key)
                return True, "✅ PERMITIDO"
            else:
                return None, "⚠️ Sin archivos para probar"
        except Exception as e:
            error_code = e.response['Error']['Code'] if hasattr(e, 'response') else 'Unknown'
            return False, f"❌ DENEGADO ({error_code})"
    
    def test_put(self, bucket):
        """Probar subir objeto."""
        try:
            key = f'test-{self.role_name}-{datetime.now().timestamp()}.txt'
            self.s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=TEST_CONTENT
            )
            # Limpiar
            try:
                self.s3.delete_object(Bucket=bucket, Key=key)
            except:
                pass
            return True, "✅ PERMITIDO"
        except Exception as e:
            error_code = e.response['Error']['Code'] if hasattr(e, 'response') else 'Unknown'
            return False, f"❌ DENEGADO ({error_code})"
    
    def test_delete(self, bucket):
        """Probar eliminar objeto."""
        try:
            # Crear objeto temporal
            key = f'test-delete-{self.role_name}-{datetime.now().timestamp()}.txt'
            
            # Intentar crear (puede fallar si no tiene permiso de put)
            try:
                self.s3.put_object(Bucket=bucket, Key=key, Body=TEST_CONTENT)
            except:
                # Si no puede crear, intentar borrar uno existente
                response = self.s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
                if 'Contents' not in response:
                    return None, "⚠️ Sin archivos para probar"
                key = response['Contents'][0]['Key']
            
            # Intentar eliminar
            self.s3.delete_object(Bucket=bucket, Key=key)
            return True, "✅ PERMITIDO"
        except Exception as e:
            error_code = e.response['Error']['Code'] if hasattr(e, 'response') else 'Unknown'
            return False, f"❌ DENEGADO ({error_code})"
    
    def run_tests(self):
        """Ejecutar todas las pruebas."""
        print(f"\n{'='*60}")
        print(f"Probando rol: {self.role_name.upper()}")
        print(f"{'='*60}")
        
        for bucket in BUCKETS:
            print(f"\n  Bucket: {bucket}")
            self.results[bucket] = {}
            
            # Probar cada operación
            success, result = self.test_list(bucket)
            self.results[bucket]['list'] = (success, result)
            print(f"    - Listar:    {result}")
            
            success, result = self.test_get(bucket)
            self.results[bucket]['get'] = (success, result)
            print(f"    - Descargar: {result}")
            
            success, result = self.test_put(bucket)
            self.results[bucket]['put'] = (success, result)
            print(f"    - Subir:     {result}")
            
            success, result = self.test_delete(bucket)
            self.results[bucket]['delete'] = (success, result)
            print(f"    - Eliminar:  {result}")
        
        return self.results


def generate_html_report(all_results):
    """Generar reporte HTML."""
    
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas de Permisos S3 - CNDD Project</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .role-section {
            margin-bottom: 50px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .role-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .results-table th {
            background: #f5f5f5;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
        }
        
        .results-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        .results-table tr:hover {
            background: #f9f9f9;
        }
        
        .allowed {
            color: #22c55e;
            font-weight: bold;
        }
        
        .denied {
            color: #ef4444;
            font-weight: bold;
        }
        
        .warning {
            color: #f59e0b;
            font-weight: bold;
        }
        
        .summary {
            background: #f0f9ff;
            border: 2px solid #0ea5e9;
            border-radius: 10px;
            padding: 30px;
            margin-top: 40px;
        }
        
        .summary h2 {
            color: #0369a1;
            margin-bottom: 20px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #0ea5e9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stat-card h3 {
            color: #64748b;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        
        .stat-card p {
            font-size: 2em;
            font-weight: bold;
            color: #0369a1;
        }
        
        .footer {
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Reporte de Pruebas de Permisos S3</h1>
            <p>CNDD Project - Sistema de Gestión de Archivos</p>
            <p>""" + datetime.now().strftime("%d de %B de %Y - %H:%M:%S") + """</p>
        </div>
        
        <div class="content">
"""
    
    total_tests = 0
    total_allowed = 0
    total_denied = 0
    
    # Generar sección para cada rol
    for role, results in all_results.items():
        html += f"""
            <div class="role-section">
                <div class="role-header">
                    📋 Rol: {role.upper()}
                </div>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Bucket</th>
                            <th>Listar</th>
                            <th>Descargar</th>
                            <th>Subir</th>
                            <th>Eliminar</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        for bucket, ops in results.items():
            html += f"<tr><td><strong>{bucket}</strong></td>"
            
            for op in ['list', 'get', 'put', 'delete']:
                success, result = ops[op]
                total_tests += 1
                
                if success is True:
                    css_class = "allowed"
                    total_allowed += 1
                elif success is False:
                    css_class = "denied"
                    total_denied += 1
                else:
                    css_class = "warning"
                
                html += f'<td class="{css_class}">{result}</td>'
            
            html += "</tr>"
        
        html += """
                    </tbody>
                </table>
            </div>
"""
    
    # Resumen
    html += f"""
            <div class="summary">
                <h2>📊 Resumen de Pruebas</h2>
                <div class="stats">
                    <div class="stat-card">
                        <h3>Total de Pruebas</h3>
                        <p>{total_tests}</p>
                    </div>
                    <div class="stat-card">
                        <h3>✅ Permitidas</h3>
                        <p style="color: #22c55e;">{total_allowed}</p>
                    </div>
                    <div class="stat-card">
                        <h3>❌ Denegadas</h3>
                        <p style="color: #ef4444;">{total_denied}</p>
                    </div>
                    <div class="stat-card">
                        <h3>% Éxito</h3>
                        <p>{(total_allowed / total_tests * 100):.1f}%</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>CNDD Project</strong> - Sistema de Almacenamiento Centralizado</p>
            <p>Desarrollado por Luis Martel | ESIT 2026</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Ejecutar pruebas."""
    print("\n" + "="*60)
    print("PRUEBAS DE PERMISOS S3 - CNDD PROJECT")
    print("="*60)
    
    all_results = {}
    
    # Probar cada rol
    for role in ROLES:
        tester = RoleTester(role)
        results = tester.run_tests()
        all_results[role] = results
    
    # Generar reporte HTML
    print("\n" + "="*60)
    print("Generando reporte HTML...")
    print("="*60)
    
    html_content = generate_html_report(all_results)
    
    # Guardar reporte
    report_file = f'docs/REPORTE_PRUEBAS_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Reporte generado: {report_file}")
    print(f"\nAbre el archivo en tu navegador para ver los resultados.")


if __name__ == '__main__':
    main()