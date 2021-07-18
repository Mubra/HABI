from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from .models import (Inmueble)

User = get_user_model()


class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('estado', 'cuidad', 'entidad', 'precio')
    ordering = ('estado', 'cuidad', 'entidad', 'precio')
    search_fields = ('estado', 'entidad__nombre', 'precio')


admin.site.unregister(User)
admin.site.register(Inmueble, InmuebleAdmin)
