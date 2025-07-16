"""
URL configuration for CasoDeEstudioParalelas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

# Generador personalizado para añadir prefijo api/ a todos los paths
class PrefixedSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Modificar las rutas para añadir el prefijo 'api/'
        paths = schema.paths
        prefixed_paths = {}
        for path_name, path_object in paths.items():
            if not path_name.startswith('/api/'):
                prefixed_paths[f'/api{path_name}'] = path_object
        
        # Reemplazar las rutas con las nuevas prefijadas
        for prefixed_path, path_object in prefixed_paths.items():
            paths[prefixed_path] = path_object
            paths.pop(prefixed_path.replace('/api', ''), None)
        
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title="API de Proveedores",
        default_version='v1',
        description="""
      API para gestionar proveedores y materiales.
      
      **Autenticación**: Obtén un token de http://ec2-3-140-254-107.us-east-2.compute.amazonaws.com/api/auth/login/
      e inclúyelo en cada solicitud como un encabezado:
      
      Authorization: Bearer tu_token_jwt
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
    ),
    generator_class=PrefixedSchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path('schema/', schema_view.with_ui(cache_timeout=0), name='schema-json'),
    
    path('api/', include('proveedores.urls')),
]
