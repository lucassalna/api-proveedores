from rest_framework import routers
from .api import ProveedorViewSet, RequisicionViewSet, PedidoViewSet
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

router.register('api/proveedores', ProveedorViewSet, 'proveedores')
router.register('api/requisiciones', RequisicionViewSet, 'requisiciones')
router.register('api/pedidos', PedidoViewSet, 'pedidos')

# Configuración de la documentación con drf-yasg
schema_view = get_schema_view(
   openapi.Info(
      title="Proveedores API",
      default_version='v1',
      description="API para gestionar proveedores y materiales",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = router.urls
urlpatterns += [
    # Documentación de la API con Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]