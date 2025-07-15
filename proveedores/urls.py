from rest_framework import routers
from .api import ProveedorViewSet, RequisicionViewSet, PedidoViewSet
from django.urls import path, include

# Crear un router
router = routers.DefaultRouter()

# Registrar tus ViewSets
router.register('proveedores', ProveedorViewSet, 'proveedores')
router.register('requisiciones', RequisicionViewSet, 'requisiciones')
router.register('pedidos', PedidoViewSet, 'pedidos')

app_name = 'proveedores'

# Usar las URLs generadas por el router
urlpatterns = router.urls