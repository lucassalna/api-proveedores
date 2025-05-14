from rest_framework import serializers
from .models import Proveedor

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