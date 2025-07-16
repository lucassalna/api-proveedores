from .models import Proveedor, Requisicion, Pedido
from .serializers import ProveedorSerializer, RequisicionSerializer, PedidoSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .services import ProveedorService, PedidoService

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['material']
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'precio', 'tiempo_de_respuesta']

    @action(detail=False, methods=['get'])
    def busqueda_avanzada(self, request):
        """/api/proveedores/busqueda_avanzada/?material= &q= &min= &max= &ordering=
        los valores son opcionales"""
        material = request.query_params.get('material')
        search_query = request.query_params.get('q')
        min_precio = request.query_params.get('min')
        max_precio = request.query_params.get('max')
        order_by = request.query_params.get('ordering')
        
        # Convertir a flotantes si están presentes
        if min_precio:
            try:
                min_precio = float(min_precio)
            except ValueError:
                return Response(
                    {"error": "El precio mínimo debe ser un valor numérico"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        if max_precio:
            try:
                max_precio = float(max_precio)
            except ValueError:
                return Response(
                    {"error": "El precio máximo debe ser un valor numérico"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        proveedores = ProveedorService.filter_proveedores(
            material=material,
            search_query=search_query,
            min_precio=min_precio,
            max_precio=max_precio,
            order_by=order_by
        )
        
        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)
    
class RequisicionViewSet(viewsets.ModelViewSet):
    queryset = Requisicion.objects.all()
    serializer_class = RequisicionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        requisicion = serializer.save()
        
        # Asignar proveedor y crear pedido
        pedido = PedidoService.asignar_proveedor(requisicion)
        
        if pedido:
            return Response({
                'requisicion': RequisicionSerializer(requisicion).data,
                'pedido': PedidoSerializer(pedido).data
            }, status=status.HTTP_201_CREATED)
        else:
            requisicion.delete()  # Eliminar la requisición si no se encontró proveedor
            return Response({
                'requisicion': RequisicionSerializer(requisicion).data,
                'error': 'No se encontró un proveedor adecuado'
            }, status=status.HTTP_201_CREATED)
        
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head', "delete", "post"]  # Solo permitir métodos GET
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Permitir filtrado por fecha
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_creacion__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_creacion__lte=fecha_fin)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)