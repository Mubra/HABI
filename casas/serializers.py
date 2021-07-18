# pylint: disable=W0223
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import \
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from .models import (Inmueble)

User = get_user_model()


class InmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inmueble
        fields = '__all__'


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    # g_recaptcha_response = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        usr = User.objects.get(username=user)

        # Add custom claims
        # groups
        token['groups'] = list(usr.groups.values_list('name', flat=True))

        return token


class HealthSerializer(serializers.Serializer):
    hostname = serializers.CharField()
    product_name = serializers.CharField()
    product_version = serializers.CharField()
    message = serializers.CharField()
