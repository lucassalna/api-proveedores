from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=r'^\d{10}$', message="El número de teléfono debe tener 10 dígitos.")]
        )
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    material = models.CharField(max_length=25)
    precio = models.DecimalField(max_digits=10, decimal_places=0, help_text="Precio por 100 kg")
    tiempo_de_respuesta = models.IntegerField(help_text="Tiempo de respuesta en días")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre