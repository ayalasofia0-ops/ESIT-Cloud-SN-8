import json
import boto3
import gzip
import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# ============================================
# VARIABLES DE ENTORNO
# Lambda lee estas variables desde la configuración
# de la función en AWS (no desde .env local)
# ============================================
REGION = os.environ.get('AWS_REGION', 'us-east-2')
OPENSEARCH_ENDPOINT = os.environ.get('OPENSEARCH_ENDPOINT')
INDEX_NAME = os.environ.get('OPENSEARCH_INDEX_NAME', 'cloudtrail-logs')

# Validar variables requeridas
if not OPENSEARCH_ENDPOINT:
    raise ValueError("Variable de entorno OPENSEARCH_ENDPOINT no configurada")

# Cliente de S3
s3 = boto3.client('s3', region_name=REGION)

# Autenticación para OpenSearch usando el rol IAM de Lambda
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
    hosts=[{'host': OPENSEARCH_ENDPOINT, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def lambda_handler(event, context):
    """Procesa logs de CloudTrail desde S3 y los envía a OpenSearch"""

    total_eventos = 0

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f"Procesando: s3://{bucket}/{key}")

        try:
            # Descargar archivo de S3
            response = s3.get_object(Bucket=bucket, Key=key)

            # Descomprimir (CloudTrail guarda logs en gzip)
            with gzip.GzipFile(fileobj=response['Body']) as gzipfile:
                content = gzipfile.read()

            # Parsear JSON
            log_data = json.loads(content)
            events = log_data.get('Records', [])

            for event_record in events:
                # Preparar documento para OpenSearch
                doc = {
                    'timestamp':            event_record.get('eventTime'),
                    'event_name':           event_record.get('eventName'),
                    'event_source':         event_record.get('eventSource'),
                    'user_identity':        event_record.get('userIdentity', {}).get('principalId'),
                    'user_type':            event_record.get('userIdentity', {}).get('type'),
                    'user_arn':             event_record.get('userIdentity', {}).get('arn'),
                    'source_ip':            event_record.get('sourceIPAddress'),
                    'user_agent':           event_record.get('userAgent'),
                    'request_parameters':   event_record.get('requestParameters'),
                    'response_elements':    event_record.get('responseElements'),
                    'error_code':           event_record.get('errorCode'),
                    'error_message':        event_record.get('errorMessage'),
                    'resources':            event_record.get('resources', []),
                    'region':               event_record.get('awsRegion'),
                    'event_id':             event_record.get('eventID'),
                    'event_type':           event_record.get('eventType'),
                    'read_only':            event_record.get('readOnly'),
                }

                # Indexar en OpenSearch
                opensearch_client.index(
                    index=INDEX_NAME,
                    body=doc,
                    id=event_record.get('eventID')
                )

                total_eventos += 1

            print(f"✓ Procesados {len(events)} eventos de {key}")

        except Exception as e:
            print(f"✗ Error procesando {key}: {str(e)}")
            raise e

    print(f"\n✅ Total eventos indexados: {total_eventos}")

    return {
        'statusCode': 200,
        'body': json.dumps(f'Procesados {total_eventos} eventos exitosamente')
    }