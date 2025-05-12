from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    material = models.TextField(max_length=25)
    precio = models.CharField(max_length=10)
    tiempo_de_respuesta = models.CharField(max_length=10)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre