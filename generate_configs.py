#!/usr/bin/env python3
"""
Script para generar archivos de configuración AWS desde variables de entorno
Uso: python generate_configs.py
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Detectar la raíz del proyecto (donde está el .env)
PROJECT_ROOT = Path(__file__).parent.absolute()

# Cargar variables de entorno desde la raíz del proyecto
env_path = PROJECT_ROOT / '.env'
if not env_path.exists():
    raise FileNotFoundError(f"No se encontró archivo .env en {PROJECT_ROOT}")

load_dotenv(env_path)

print(f"📂 Raíz del proyecto: {PROJECT_ROOT}")
print(f"📄 Usando .env de: {env_path}\n")

# Crear directorios si no existen
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# Obtener variable de entorno
def get_env(key, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Variable de entorno {key} no encontrada en .env")
    return value

# Guardar JSON
def save_json(data, filepath):
    # Convertir a ruta absoluta basada en PROJECT_ROOT
    full_path = PROJECT_ROOT / filepath
    ensure_dir(full_path.parent)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✓ {filepath}")


def generate_all_configs():
    """Genera todos los archivos de configuración"""
    
    base_dir = "aws-config"
    
    # Variables comunes
    account_id = get_env('AWS_ACCOUNT_ID')
    region = get_env('AWS_REGION')
    bucket_publica = get_env('BUCKET_PUBLICA')
    bucket_proyectos = get_env('BUCKET_PROYECTOS')
    bucket_rrhh = get_env('BUCKET_RRHH')
    
    # ===========================================
    # POLÍTICAS IAM
    # ===========================================
    
    # Policy: Solo Lectura
    policy_solo_lectura = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "ListarBuckets",
            "Effect": "Allow",
            "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
            "Resource": "*"
        }, {
            "Sid": "SoloLectura",
            "Effect": "Allow",
            "Action": ["s3:ListBucket", "s3:GetObjectAttributes", "s3:GetObjectMetadata"],
            "Resource": [
                f"arn:aws:s3:::{bucket_publica}",
                f"arn:aws:s3:::{bucket_publica}/*",
                f"arn:aws:s3:::{bucket_proyectos}",
                f"arn:aws:s3:::{bucket_proyectos}/*",
                f"arn:aws:s3:::{bucket_rrhh}",
                f"arn:aws:s3:::{bucket_rrhh}/*"
            ]
        }]
    }
    save_json(policy_solo_lectura, f"{base_dir}/policies/policy-solo-lectura.json")
    
    # Policy: Lectura y Escritura
    policy_lectura_escritura = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "ListarBuckets",
            "Effect": "Allow",
            "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
            "Resource": "*"
        }, {
            "Sid": "LecturaEscritura",
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
            "Resource": [
                f"arn:aws:s3:::{bucket_publica}",
                f"arn:aws:s3:::{bucket_publica}/*",
                f"arn:aws:s3:::{bucket_proyectos}",
                f"arn:aws:s3:::{bucket_proyectos}/*",
                f"arn:aws:s3:::{bucket_rrhh}",
                f"arn:aws:s3:::{bucket_rrhh}/*"
            ]
        }]
    }
    save_json(policy_lectura_escritura, f"{base_dir}/policies/policy-lectura-escritura.json")
    
    # Policy: Solo Carga
    policy_solo_carga = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "ListarBuckets",
            "Effect": "Allow",
            "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
            "Resource": "*"
        }, {
            "Sid": "SoloCarga",
            "Effect": "Allow",
            "Action": ["s3:PutObject"],
            "Resource": [
                f"arn:aws:s3:::{bucket_publica}/*",
                f"arn:aws:s3:::{bucket_proyectos}/*",
                f"arn:aws:s3:::{bucket_rrhh}/*"
            ]
        }]
    }
    save_json(policy_solo_carga, f"{base_dir}/policies/policy-solo-carga.json")
    
    # Policy: Solo Descarga
    policy_solo_descarga = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "ListarBuckets",
            "Effect": "Allow",
            "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
            "Resource": "*"
        }, {
            "Sid": "SoloDescarga",
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": [
                f"arn:aws:s3:::{bucket_publica}",
                f"arn:aws:s3:::{bucket_publica}/*",
                f"arn:aws:s3:::{bucket_proyectos}",
                f"arn:aws:s3:::{bucket_proyectos}/*",
                f"arn:aws:s3:::{bucket_rrhh}",
                f"arn:aws:s3:::{bucket_rrhh}/*"
            ]
        }]
    }
    save_json(policy_solo_descarga, f"{base_dir}/policies/policy-solo-descarga.json")
    
    # Policy: Admin
    policy_admin = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "ListarTodosLosBuckets",
            "Effect": "Allow",
            "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
            "Resource": "*"
        }, {
            "Sid": "AccesoCompletoS3",
            "Effect": "Allow",
            "Action": ["s3:*"],
            "Resource": [
                f"arn:aws:s3:::{bucket_publica}",
                f"arn:aws:s3:::{bucket_publica}/*",
                f"arn:aws:s3:::{bucket_proyectos}",
                f"arn:aws:s3:::{bucket_proyectos}/*",
                f"arn:aws:s3:::{bucket_rrhh}",
                f"arn:aws:s3:::{bucket_rrhh}/*",
                f"arn:aws:s3:::{get_env('BUCKET_LOGS')}",
                f"arn:aws:s3:::{get_env('BUCKET_LOGS')}/*"
            ]
        }, {
            "Sid": "VerLogs",
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:GetLogEvents"
            ],
            "Resource": "*"
        }]
    }
    save_json(policy_admin, f"{base_dir}/policies/policy-admin.json")
    
    # ===========================================
    # COGNITO
    # ===========================================
    
    # Cognito User Pool
    cognito_user_pool = {
        "PoolName": get_env('COGNITO_USER_POOL_NAME'),
        "Policies": {
            "PasswordPolicy": {
                "MinimumLength": 8,
                "RequireUppercase": True,
                "RequireLowercase": True,
                "RequireNumbers": True,
                "RequireSymbols": False
            }
        },
        "AutoVerifiedAttributes": ["email"],
        "UsernameAttributes": ["email"],
        "UsernameConfiguration": {"CaseSensitive": False},
        "Schema": [
            {
                "Name": "email",
                "AttributeDataType": "String",
                "Required": True,
                "Mutable": True
            },
            {
                "Name": "name",
                "AttributeDataType": "String",
                "Required": True,
                "Mutable": True
            }
        ],
        "AccountRecoverySetting": {
            "RecoveryMechanisms": [
                {"Priority": 1, "Name": "verified_email"}
            ]
        }
    }
    save_json(cognito_user_pool, f"{base_dir}/cognito/cognito-user-pool.json")
    
    # Cognito Identity Pool
    cognito_identity_pool = {
        "IdentityPoolName": get_env('COGNITO_IDENTITY_POOL_NAME'),
        "AllowUnauthenticatedIdentities": False,
        "CognitoIdentityProviders": [{
            "ProviderName": f"cognito-idp.{region}.amazonaws.com/{get_env('COGNITO_USER_POOL_ID')}",
            "ClientId": get_env('COGNITO_CLIENT_ID'),
            "ServerSideTokenCheck": False
        }]
    }
    save_json(cognito_identity_pool, f"{base_dir}/cognito/cognito-identity-pool.json")
    
    # Cognito Trust Policy
    cognito_trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Federated": "cognito-identity.amazonaws.com"},
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    f"cognito-identity.amazonaws.com:aud": get_env('COGNITO_IDENTITY_POOL_ID')
                },
                "ForAnyValue:StringLike": {
                    f"cognito-identity.amazonaws.com:amr": "authenticated"
                }
            }
        }]
    }
    save_json(cognito_trust_policy, f"{base_dir}/policies/cognito-trust-policy.json")
    
    # Identity Pool Roles
    identity_pool_roles = {
        "IdentityPoolId": get_env('COGNITO_IDENTITY_POOL_ID'),
        "Roles": {
            "authenticated": f"arn:aws:iam::{account_id}:role/{get_env('ROLE_LECTURA_ESCRITURA')}"
        },
        "RoleMappings": {
            f"cognito-idp.{region}.amazonaws.com/{get_env('COGNITO_USER_POOL_ID')}:{get_env('COGNITO_CLIENT_ID')}": {
                "Type": "Token",
                "AmbiguousRoleResolution": "Deny"
            }
        }
    }
    save_json(identity_pool_roles, f"{base_dir}/cognito/identity-pool-roles.json")
    
    # ===========================================
    # OPENSEARCH
    # ===========================================
    
    opensearch_domain = {
        "DomainName": get_env('OPENSEARCH_DOMAIN_NAME'),
        "EngineVersion": "OpenSearch_2.11",
        "ClusterConfig": {
            "InstanceType": "t3.small.search",
            "InstanceCount": 1,
            "DedicatedMasterEnabled": False,
            "ZoneAwarenessEnabled": False
        },
        "EBSOptions": {
            "EBSEnabled": True,
            "VolumeType": "gp3",
            "VolumeSize": 10
        },
        "AccessPolicies": json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "es:*",
                "Resource": f"arn:aws:es:{region}:{account_id}:domain/{get_env('OPENSEARCH_DOMAIN_NAME')}/*"
            }]
        }),
        "EncryptionAtRestOptions": {"Enabled": True},
        "NodeToNodeEncryptionOptions": {"Enabled": True},
        "DomainEndpointOptions": {"EnforceHTTPS": True},
        "AdvancedSecurityOptions": {
            "Enabled": True,
            "InternalUserDatabaseEnabled": True,
            "MasterUserOptions": {
                "MasterUserName": get_env('OPENSEARCH_MASTER_USER'),
                "MasterUserPassword": get_env('OPENSEARCH_MASTER_PASSWORD')
            }
        }
    }
    save_json(opensearch_domain, f"{base_dir}/opensearch/opensearch-domain.json")
    
    # ===========================================
    # LIFECYCLE POLICIES
    # ===========================================
    
    # Lifecycle: Bucket Público
    lifecycle_publica = {
        "Rules": [
            {
                "ID": "TransicionAlmacenamientoPublico",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "Transitions": [
                    {"Days": 30, "StorageClass": "STANDARD_IA"},
                    {"Days": 90, "StorageClass": "GLACIER_IR"}
                ]
            },
            {
                "ID": "LimpiezaVersionesAntiguas",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "NoncurrentVersionExpiration": {"NoncurrentDays": 30},
                "Expiration": {"ExpiredObjectDeleteMarker": True}
            }
        ]
    }
    save_json(lifecycle_publica, f"{base_dir}/lifecycle/lifecycle-publica.json")
    
    # Lifecycle: Bucket Proyectos
    lifecycle_proyectos = {
        "Rules": [
            {
                "ID": "TransicionAlmacenamientoProyectos",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "Transitions": [
                    {"Days": 45, "StorageClass": "STANDARD_IA"},
                    {"Days": 120, "StorageClass": "GLACIER_IR"}
                ]
            },
            {
                "ID": "LimpiezaVersionesAntiguas",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "NoncurrentVersionExpiration": {"NoncurrentDays": 60},
                "Expiration": {"ExpiredObjectDeleteMarker": True}
            }
        ]
    }
    save_json(lifecycle_proyectos, f"{base_dir}/lifecycle/lifecycle-proyectos.json")
    
    # Lifecycle: Bucket RRHH
    lifecycle_rrhh = {
        "Rules": [
            {
                "ID": "TransicionAlmacenamientoRRHH",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "Transitions": [
                    {"Days": 60, "StorageClass": "STANDARD_IA"},
                    {"Days": 180, "StorageClass": "GLACIER_IR"}
                ]
            },
            {
                "ID": "LimpiezaVersionesAntiguas",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "NoncurrentVersionExpiration": {"NoncurrentDays": 90},
                "Expiration": {"ExpiredObjectDeleteMarker": True}
            }
        ]
    }
    save_json(lifecycle_rrhh, f"{base_dir}/lifecycle/lifecycle-rrhh.json")
    
    # ===========================================
    # LOGGING CONFIGURATIONS
    # ===========================================
    
    bucket_logs = get_env('BUCKET_LOGS')
    
    logging_publica = {
        "LoggingEnabled": {
            "TargetBucket": bucket_logs,
            "TargetPrefix": "logs-publica/"
        }
    }
    save_json(logging_publica, f"{base_dir}/logging/logging-publica.json")
    
    logging_proyectos = {
        "LoggingEnabled": {
            "TargetBucket": bucket_logs,
            "TargetPrefix": "logs-proyectos/"
        }
    }
    save_json(logging_proyectos, f"{base_dir}/logging/logging-proyectos.json")
    
    logging_rrhh = {
        "LoggingEnabled": {
            "TargetBucket": bucket_logs,
            "TargetPrefix": "logs-rrhh/"
        }
    }
    save_json(logging_rrhh, f"{base_dir}/logging/logging-rrhh.json")
    
    # ===========================================
    # BUCKET POLICIES
    # ===========================================
    
    # Bucket Policy: Público
    bucket_policy_publica = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "RequireSecureTransport",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    f"arn:aws:s3:::{bucket_publica}",
                    f"arn:aws:s3:::{bucket_publica}/*"
                ],
                "Condition": {
                    "Bool": {"aws:SecureTransport": "false"}
                }
            },
            {
                "Sid": "AllowAuthenticatedAccess",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_publica}",
                    f"arn:aws:s3:::{bucket_publica}/*"
                ],
                "Condition": {
                    "StringLike": {
                        "aws:userid": f"arn:aws:sts::{account_id}:assumed-role/Cognito-*"
                    }
                }
            }
        ]
    }
    save_json(bucket_policy_publica, f"{base_dir}/policies/bucket-policy-publica.json")
    
    # Bucket Policy: Proyectos
    bucket_policy_proyectos = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "RequireSecureTransport",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    f"arn:aws:s3:::{bucket_proyectos}",
                    f"arn:aws:s3:::{bucket_proyectos}/*"
                ],
                "Condition": {
                    "Bool": {"aws:SecureTransport": "false"}
                }
            },
            {
                "Sid": "AllowAuthenticatedAccess",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_proyectos}",
                    f"arn:aws:s3:::{bucket_proyectos}/*"
                ],
                "Condition": {
                    "StringLike": {
                        "aws:userid": f"arn:aws:sts::{account_id}:assumed-role/Cognito-*"
                    }
                }
            }
        ]
    }
    save_json(bucket_policy_proyectos, f"{base_dir}/policies/bucket-policy-proyectos.json")
    
    # Bucket Policy: RRHH
    bucket_policy_rrhh = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "RequireSecureTransport",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    f"arn:aws:s3:::{bucket_rrhh}",
                    f"arn:aws:s3:::{bucket_rrhh}/*"
                ],
                "Condition": {
                    "Bool": {"aws:SecureTransport": "false"}
                }
            },
            {
                "Sid": "AllowAuthenticatedAccess",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_rrhh}",
                    f"arn:aws:s3:::{bucket_rrhh}/*"
                ],
                "Condition": {
                    "StringLike": {
                        "aws:userid": f"arn:aws:sts::{account_id}:assumed-role/Cognito-*"
                    }
                }
            }
        ]
    }
    save_json(bucket_policy_rrhh, f"{base_dir}/policies/bucket-policy-rrhh.json")
    
    # Bucket Policy: CloudTrail Logs
    bucket_cloudtrail_logs = get_env('BUCKET_CLOUDTRAIL_LOGS')
    cloudtrail_name = get_env('CLOUDTRAIL_NAME')
    
    cloudtrail_bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_cloudtrail_logs}"
            },
            {
                "Sid": "AWSCloudTrailWrite",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_cloudtrail_logs}/AWSLogs/{account_id}/*",
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control",
                        "aws:SourceArn": f"arn:aws:cloudtrail:{region}:{account_id}:trail/{cloudtrail_name}"
                    }
                }
            }
        ]
    }
    save_json(cloudtrail_bucket_policy, f"{base_dir}/policies/cloudtrail-bucket-policy.json")
    
    # ===========================================
    # CLOUDTRAIL
    # ===========================================
    
    cloudtrail_event_selectors = {
        "TrailName": cloudtrail_name,
        "EventSelectors": [
            {
                "ReadWriteType": "All",
                "IncludeManagementEvents": True,
                "DataResources": [
                    {
                        "Type": "AWS::S3::Object",
                        "Values": [
                            f"arn:aws:s3:::{bucket_publica}/*",
                            f"arn:aws:s3:::{bucket_proyectos}/*",
                            f"arn:aws:s3:::{bucket_rrhh}/*"
                        ]
                    }
                ]
            }
        ]
    }
    save_json(cloudtrail_event_selectors, f"{base_dir}/cloudtrail/cloudtrail-event-selectors.json")
    
    # ===========================================
    # LAMBDA FUNCTION
    # ===========================================
    
    lambda_code = f'''import json
import boto3
import gzip
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Configuración
REGION = '{region}'
OPENSEARCH_ENDPOINT = '{get_env('OPENSEARCH_ENDPOINT')}'
INDEX_NAME = '{get_env('OPENSEARCH_INDEX_NAME')}'

# Cliente de S3
s3 = boto3.client('s3')

# Autenticación para OpenSearch
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    REGION,
    'es',
    session_token=credentials.token
)

# Cliente de OpenSearch
opensearch_client = OpenSearch(
    hosts=[{{'host': OPENSEARCH_ENDPOINT, 'port': 443}}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def lambda_handler(event, context):
    """Procesa logs de CloudTrail desde S3 y los envía a OpenSearch"""
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Procesando: s3://{{bucket}}/{{key}}")
        
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            
            with gzip.GzipFile(fileobj=response['Body']) as gzipfile:
                content = gzipfile.read()
            
            log_data = json.loads(content)
            events = log_data.get('Records', [])
            
            for event_record in events:
                doc = {{
                    'timestamp': event_record.get('eventTime'),
                    'event_name': event_record.get('eventName'),
                    'event_source': event_record.get('eventSource'),
                    'user_identity': event_record.get('userIdentity', {{}}).get('principalId'),
                    'source_ip': event_record.get('sourceIPAddress'),
                    'user_agent': event_record.get('userAgent'),
                    'request_parameters': event_record.get('requestParameters'),
                    'response_elements': event_record.get('responseElements'),
                    'error_code': event_record.get('errorCode'),
                    'error_message': event_record.get('errorMessage'),
                    'resources': event_record.get('resources', []),
                    'region': event_record.get('awsRegion'),
                    'event_id': event_record.get('eventID')
                }}
                
                opensearch_client.index(
                    index=INDEX_NAME,
                    body=doc,
                    id=event_record.get('eventID')
                )
            
            print(f"✓ Procesados {{len(events)}} eventos de {{key}}")
            
        except Exception as e:
            print(f"✗ Error procesando {{key}}: {{str(e)}}")
            raise e
    
    return {{
        'statusCode': 200,
        'body': json.dumps('Logs procesados exitosamente')
    }}
'''
    
    # Guardar archivo Lambda (Python, no JSON)
    lambda_path = PROJECT_ROOT / f"{base_dir}/lambda/cloudtrail_to_opensearch.py"
    ensure_dir(lambda_path.parent)
    with open(lambda_path, 'w', encoding='utf-8') as f:
        f.write(lambda_code)
    print(f"✓ {base_dir}/lambda/cloudtrail_to_opensearch.py")
    
    print("\n" + "="*60)
    print("✅ TODOS LOS ARCHIVOS DE CONFIGURACIÓN GENERADOS!")
    print("="*60)
    print(f"\n📁 Ubicación: {PROJECT_ROOT / base_dir}")
    print("\n📋 Estructura creada:")
    print("   ├── policies/        (10 archivos)")
    print("   ├── lifecycle/       (3 archivos)")
    print("   ├── logging/         (3 archivos)")
    print("   ├── cognito/         (3 archivos)")
    print("   ├── opensearch/      (1 archivo)")
    print("   ├── cloudtrail/      (1 archivo)")
    print("   └── lambda/          (1 archivo)")
    print("\n💡 Total: 22 archivos de configuración generados")
    print(f"\n✨ Los archivos existentes fueron sobrescritos")


if __name__ == "__main__":
    try:
        generate_all_configs()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)
