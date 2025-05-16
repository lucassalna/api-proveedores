from .models import Proveedor,Pedido
class AsignacionService:
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
            
            # Crear pedido
            pedido = Pedido.objects.create(
                proveedor=mejor_proveedor,
                requisicion=requisicion,
                precio_total=precio_total,
                tiempo_respuesta=mejor_proveedor.tiempo_de_respuesta
            )
            return pedido
        
        return None