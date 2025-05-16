from rest_framework import serializers
from .models import Proveedor, Requisicion, Pedido
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
        read_only_fields = ('fecha_registro', )

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")

        return value
    
    def validate_tiempo_de_respuesta(self, value):
        if value <= 0:
            raise serializers.ValidationError("El tiempo de respuesta debe ser mayor que cero.")

        return value
    
class RequisicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisicion
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor', 'proveedor_nombre', 'requisicion', 
                 'precio_total', 'tiempo_respuesta', 'fecha_creacion']