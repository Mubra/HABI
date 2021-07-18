from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Estado(models.Model):
    '''
    Modelo Estados de la Republica
    '''

    nombre = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    '''
    Modelo Cuidades
    '''

    nombre = models.CharField(max_length=80, null=False, blank=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Inmueble(models.Model):
    PRE_V = 0
    EN_V = 1
    V = 2
    CHOICES_3STATE = (
        (PRE_V, 'pre_venta'),
        (EN_V, 'en_venta'),
        (V, 'vendido')
    )
    '''
    Modelo para Inmueble
    '''
    descripcion = models.CharField(max_length=80, null=False, blank=False)
    contruccion_anio = models.IntegerField("Año del construcción", null=True, blank=True,
                                           validators=[MinValueValidator(1950),
                                                       MaxValueValidator(2021)])
    entidad = models.ForeignKey(Estado, on_delete=models.CASCADE,
                                verbose_name='Entidad federativa', null=True, blank=True)
    # Se puede manejar igual que estado para manejar una modelo relacional mas optimo.
    cuidad = models.ForeignKey(Ciudad, on_delete=models.CASCADE,
                               verbose_name='Cuidad', null=True, blank=True)
    estado = models.PositiveIntegerField("Estado de la propiedad",
                                         choices=CHOICES_3STATE, null=True, blank=True,
                                         validators=[MinValueValidator(0)])
    precio = models.PositiveIntegerField("Precio", null=True, blank=True,
                                         validators=[MinValueValidator(1)])
    # la direccion se puede manejar con relacional de modelos "estado", "cuidad", "C.P" y
    # una pequeña descripcion para ejemplos ilustrativos se manejara como un CharField
    direccion = models.CharField(max_length=80, null=False, blank=False)
