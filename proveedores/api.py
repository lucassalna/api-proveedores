from .models import Proveedor, Requisicion
from .serializers import ProveedorSerializer, RequisicionSerializer, PedidoSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .services import ProveedorService
from . import asignacion_proveedor

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['material']
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'precio', 'tiempo_de_respuesta']
    
    def list(self, request, *args, **kwargs):
        """Sobrescribe el método list para usar el servicio"""
        # Verifica si se están usando filtros, búsqueda o ordenamiento
        if any(key in request.query_params for key in ['material', 'search', 'ordering']):
            # Si hay filtros, deja que DRF los maneje con su implementación por defecto
            return super().list(request, *args, **kwargs)
        
        # Si no hay filtros, usa el servicio
        proveedores = ProveedorService.get_all_proveedores()
        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Sobrescribe el método retrieve para usar el servicio"""
        proveedor_id = kwargs.get('pk')
        proveedor = ProveedorService.get_proveedor_by_id(proveedor_id)
        
        if not proveedor:
            return Response(
                {'error': f'No se encontró el proveedor con ID {proveedor_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(proveedor)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Sobrescribe el método create para usar el servicio"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            proveedor = ProveedorService.create_proveedor(serializer.validated_data)
            response_serializer = self.get_serializer(proveedor)
            return Response(
                response_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'Error al crear el proveedor: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        """Sobrescribe el método update para usar el servicio"""
        proveedor_id = kwargs.get('pk')
        
        # Validar datos de entrada
        serializer = self.get_serializer(data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        
        # Usar el servicio para actualizar
        proveedor = ProveedorService.update_proveedor(
            proveedor_id=proveedor_id,
            data=serializer.validated_data
        )
        
        if not proveedor:
            return Response(
                {'error': f'No se encontró el proveedor con ID {proveedor_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        response_serializer = self.get_serializer(proveedor)
        return Response(response_serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """Sobrescribe partial_update para usar el servicio"""
        # Agrega partial=True para indicar que es una actualización parcial (PATCH)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Sobrescribe el método destroy para usar el servicio"""
        proveedor_id = kwargs.get('pk')
        success = ProveedorService.delete_proveedor(proveedor_id)
        
        if not success:
            return Response(
                {'error': f'No se encontró el proveedor con ID {proveedor_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
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
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        requisicion = serializer.save()
        
        # Asignar proveedor y crear pedido
        pedido = asignacion_proveedor.AsignacionService.asignar_proveedor(requisicion)
        
        if pedido:
            return Response({
                'requisicion': RequisicionSerializer(requisicion).data,
                'pedido': PedidoSerializer(pedido).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'requisicion': RequisicionSerializer(requisicion).data,
                'error': 'No se encontró un proveedor adecuado'
            }, status=status.HTTP_201_CREATED)