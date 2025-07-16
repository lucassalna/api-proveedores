from rest_framework import authentication, exceptions
import jwt
from django.conf import settings
import requests
from django.contrib.auth.models import User

class ExternalJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Obtener el token del encabezado Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        
        try:
            #Verificar el token con el endpoint de la API externa
            response = requests.post(
                "http://ec2-3-140-254-107.us-east-2.compute.amazonaws.com/api/auth/verify/",
                json={"token": token}
            )
            
            if response.status_code != 200:
                raise exceptions.AuthenticationFailed('Token inválido o expirado')
                
            # Extraer información del token (asumiendo que es un JWT)
            # Nota: Esta verificación es mínima ya que la API externa ya verificó el token
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # Obtener o crear usuario basado en la información del token
            username = payload.get('username', payload.get('sub', 'usuario_externo'))
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Crear usuario si no existe
                user = User(username=username)
                user.is_staff = payload.get('is_staff', False)
                user.save()
                
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token inválido')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Error de autenticación: {str(e)}')