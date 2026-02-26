""" Estado Global de la Aplicacion"""

import reflex as rx 

class GlobalState(rx.State):
    """Estado Global compartido entre todas las paginas """

    #Datos del usuario Autenticado
    is_authenticated: bool = False
    username: str = ''
    name:str  = ''
    email: str = ''
    role: str = ''
    access_token: str = ''

    def login_user(self, user_data: dict):
        """Guardar datos del usuario al hacer login."""
    
        self.is_authenticated = True
        self.username = user_data.get('username', '')
        self.name = user_data.get('name', '')
        self.email = user_data.get('email', '')
        self.role = user_data.get('role', '')
        self.access_token = user_data.get('access_token', '')


    def logout(self):
        """Cerrar sesión."""
        self.is_authenticated = False
        self.username = ""
        self.email = ""
        self.role = ""


        if self.access_token:
            try: 
                import boto3
                import os
                from dotenv import load_dotenv

                load_dotenv()

                client = boto3.client(
                    'cognito-idp',
                    region_name = os.getenv('AWS_REGION')
                )

                #Cerrar sesion global en cognito
                client.global_sign_out(
                    AccessToken = self.access_token
                )

            except Exception as e:
                print(f'Error Cerrando Sesion en Cognito: {e}')

        self.access_token = ''                

        return rx.redirect("/login")