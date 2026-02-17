"""
Módulo de autenticación con AWS Cognito
"""

import os
import boto3
from typing import Optional, Dict, Tuple, List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class CognitoAuth:
    """Clase para manejar autenticación con AWS Cognito."""
    
    def __init__(self):
        """Inicializar cliente de Cognito."""
        self.region = os.getenv('AWS_REGION')
        self.user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        self.client_id = os.getenv('COGNITO_CLIENT_ID')
        
        # Cliente de Cognito
        self.client = boto3.client(
            'cognito-idp',
            region_name=self.region
        )
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Autenticar usuario con Cognito.
        
        Returns:
            Tuple (éxito, datos_usuario, mensaje_error)
        """
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            
            # Extraer tokens
            access_token = response['AuthenticationResult']['AccessToken']
            id_token = response['AuthenticationResult']['IdToken']
            
            # Obtener info del usuario y sus grupos
            user_info = self.get_user_info(access_token)
            groups = self.get_user_groups(username)
            
            # Validar que el usuario tenga un grupo asignado
            if not groups:
                return False, None, "Usuario sin grupo asignado. Contacta al administrador."
            
            # Determinar el rol principal (primer grupo)
            role = groups[0]
            
            user_data = {
                'username': username,
                'access_token': access_token,
                'id_token': id_token,
                'role': role,
                'groups': groups,
                'user_info': user_info
            }
            
            return True, user_data, None
            
        except self.client.exceptions.NotAuthorizedException:
            return False, None, "Usuario o contraseña incorrectos"
        except self.client.exceptions.UserNotFoundException:
            return False, None, "Usuario no encontrado"
        except Exception as e:
            return False, None, f"Error: {str(e)}"
    
    def get_user_info(self, access_token: str) -> Dict:
        """Obtener información del usuario."""
        try:
            response = self.client.get_user(AccessToken=access_token)
            
            user_info = {
                'username': response['Username'],
                'attributes': {}
            }
            
            for attr in response['UserAttributes']:
                user_info['attributes'][attr['Name']] = attr['Value']
            
            return user_info
            
        except Exception as e:
            print(f"Error obteniendo info: {e}")
            return {}
    
    def get_user_groups(self, username: str) -> List[str]:
        """Obtener grupos del usuario en Cognito."""
        try:
            response = self.client.admin_list_groups_for_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            
            groups = [group['GroupName'] for group in response.get('Groups', [])]
            return groups
            
        except Exception as e:
            print(f"Error obteniendo grupos: {e}")
            return []
    
    def create_user(self, username: str, password: str, email: str, group: str) -> Tuple[bool, Optional[str]]:
        """
        Crear un nuevo usuario (solo admin).
        
        Returns:
            Tuple (éxito, mensaje_error)
        """
        try:
            # Crear usuario
            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=username,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'email_verified', 'Value': 'true'}
                ],
                TemporaryPassword=password,
                MessageAction='SUPPRESS'
            )
            
            # Establecer contraseña permanente
            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=username,
                Password=password,
                Permanent=True
            )
            
            # Agregar a grupo
            if group:
                self.client.admin_add_user_to_group(
                    UserPoolId=self.user_pool_id,
                    Username=username,
                    GroupName=group
                )
            
            return True, None
            
        except Exception as e:
            return False, f"Error creando usuario: {str(e)}"
