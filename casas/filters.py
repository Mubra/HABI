from django_filters import rest_framework as filters

from .models import (Inmueble)


class InmuebleFilter(filters.FilterSet):
    class Meta:
        model = Inmueble
        fields = {
            'estado': ['exact', ],
            'descripcion':  ['exact', 'contains', 'icontains', 'in'],
            'contruccion_anio': ['gte', 'lte', 'exact', 'gt', 'lt'],
            'precio': ['gte', 'lte', 'exact', 'gt', 'lt'],
        }
