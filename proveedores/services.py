from .models import Proveedor, Pedido
from decimal import Decimal
from typing import List, Dict, Any, Optional
from django.db.models import Q
import requests
from django.http import JsonResponse

class ProveedorService:
    @staticmethod
    def filter_proveedores(material: Optional[str] = None, search_query: Optional[str] = None, 
                           min_precio: Optional[float] = None, max_precio: Optional[float] = None,
                           order_by: Optional[str] = None) -> List[Proveedor]:
        """
        Filtra proveedores por varios criterios
        """
        queryset = Proveedor.objects.all()
        
        # Aplicar filtro por material
        if material:
            queryset = queryset.filter(material=material)
        
        # Aplicar búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) | 
                Q(material__icontains=search_query)
            )
        
        # Filtrar por rango de precio
        if min_precio is not None:
            queryset = queryset.filter(precio__gte=Decimal(str(min_precio)))
        if max_precio is not None:
            queryset = queryset.filter(precio__lte=Decimal(str(max_precio)))
        
        # Ordenar resultados
        if order_by:
            # Manejar ordenamiento descendente (si comienza con '-')
            queryset = queryset.order_by(order_by)
        
        return list(queryset)
    
class PedidoService:
    @staticmethod
    def asignar_proveedor(requisicion):
        # Buscar proveedores que tengan el material solicitado
        proveedores = Proveedor.objects.filter(material__iexact=requisicion.producto)
        
        if not proveedores.exists():
            return None
            
        # Factor de urgencia para ajustar la importancia del tiempo de respuesta
        factores_urgencia = {
            'BAJA': 0.2,
            'MEDIA': 0.5,
            'ALTA': 0.8
        }
        
        factor_urgencia = factores_urgencia[requisicion.urgencia]
        
        # Encontrar el mejor proveedor
        mejor_proveedor = None
        mejor_puntuacion = float('inf')
        
        for proveedor in proveedores:
            # Calcular precio total directamente (precio unitario × cantidad)
            precio_total = float(proveedor.precio) * requisicion.cantidad
            
            # Calcular puntuación (menor es mejor)
            puntuacion = (precio_total * (1 - factor_urgencia) + 
                         proveedor.tiempo_de_respuesta * factor_urgencia)
            
            if puntuacion < mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_proveedor = proveedor
        
        if mejor_proveedor:
            # Calcular precio total final en enteros
            precio_total = mejor_proveedor.precio * requisicion.cantidad

            Pedido.objects.create(
                proveedor=mejor_proveedor,
                requisicion=requisicion,
                precio_total=precio_total,
                tiempo_respuesta=mejor_proveedor.tiempo_de_respuesta
            )

            #token para la api
            URL_token = "http://ec2-3-140-254-107.us-east-2.compute.amazonaws.com/api/auth/login/"

            data = {
                "username": "provider_service",
                "password": "provider123"
            }

            token = requests.post(URL_token, data=data).json().get('access')

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }

            # Crear pedido
            
            # URL de productos
            URL_API = "http://ec2-3-140-254-107.us-east-2.compute.amazonaws.com/api/proveedores-despachos/"

            pedido_despacho ={
                "external_order_id": Pedido.objects.last().id,
                "supplier_name": mejor_proveedor.nombre,
                "product_name": requisicion.producto,
                "quantity": requisicion.cantidad,
            }
            
            try:
                response = requests.post(URL_API, json=pedido_despacho, headers=headers)
                response.raise_for_status()  # Lanza excepción si hay error HTTP
                return pedido_despacho
            
                 
            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": str(e)}, status=500)
                
        
        return None