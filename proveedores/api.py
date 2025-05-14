from .models import Proveedor
from rest_framework import viewsets, permissions, status
from .serializers import ProveedorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .requisicion_service import RequisitionService
from .despacho_service import DispatchService

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]
    @action(detail=False, methods=['GET'])
    def get_requisition(self, request):
        """Get specific requisition details"""
        requisition_id = request.query_params.get('requisition_id')
        
        if not requisition_id:
            return Response(
                {'error': 'requisition_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            requisition = RequisitionService.get_requisition_details(requisition_id)
            return Response(requisition)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail=True, methods=['POST'])
    def send_to_dispatch(self, request, pk=None):
        """Send provider to Dispatch API"""
        provider = self.get_object()
        try:
            dispatch_data = {
                'provider_id': provider.id,
                'nombre': provider.nombre,
                'telefono': provider.telefono,
                'direccion': provider.direccion,
                'email': provider.email,
                'material': provider.material,
                'precio': provider.precio,
                'tiempo_de_respuesta': provider.tiempo_de_respuesta
            }
            result = DispatchService.send_provider_info(dispatch_data)
            return Response(result)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )