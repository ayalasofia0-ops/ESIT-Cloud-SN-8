import json
import boto3
import gzip
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Configuración
REGION = 'us-east-2'
OPENSEARCH_ENDPOINT = ''
INDEX_NAME = 'cloudtrail-logs'

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
    hosts=[{'host': OPENSEARCH_ENDPOINT, 'port': 443}],
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
        
        print(f"Procesando: s3://{bucket}/{key}")
        
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            
            with gzip.GzipFile(fileobj=response['Body']) as gzipfile:
                content = gzipfile.read()
            
            log_data = json.loads(content)
            events = log_data.get('Records', [])
            
            for event_record in events:
                doc = {
                    'timestamp': event_record.get('eventTime'),
                    'event_name': event_record.get('eventName'),
                    'event_source': event_record.get('eventSource'),
                    'user_identity': event_record.get('userIdentity', {}).get('principalId'),
                    'source_ip': event_record.get('sourceIPAddress'),
                    'user_agent': event_record.get('userAgent'),
                    'request_parameters': event_record.get('requestParameters'),
                    'response_elements': event_record.get('responseElements'),
                    'error_code': event_record.get('errorCode'),
                    'error_message': event_record.get('errorMessage'),
                    'resources': event_record.get('resources', []),
                    'region': event_record.get('awsRegion'),
                    'event_id': event_record.get('eventID')
                }
                
                opensearch_client.index(
                    index=INDEX_NAME,
                    body=doc,
                    id=event_record.get('eventID')
                )
            
            print(f"✓ Procesados {len(events)} eventos de {key}")
            
        except Exception as e:
            print(f"✗ Error procesando {key}: {str(e)}")
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps('Logs procesados exitosamente')
    }
