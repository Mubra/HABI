from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('Inmueble', views.InmuebleViewSet)

urlpatterns = [
    path('health/',
         views.HealthView.as_view(),
         name='health'),
]

urlpatterns += router.urls
