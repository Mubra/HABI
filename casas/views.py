import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from . import filters
from .models import (Inmueble)
from .pagination import StandardResultsSetPagination
from .serializers import (HealthSerializer, InmuebleSerializer, TokenObtainPairSerializer)

logger = logging.getLogger(__name__)


def healthy():
    '''
    codigo para probar que la app esta en condiciones de
    brindar servicio
    '''
    model = get_user_model()
    model.objects.all().first()


class InmuebleViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = filters.InmuebleFilter
    ordering_fields = '__all__'
    # ordering = ('nombre',)
    # search_fields = ('nombre',)
    pagination_class = StandardResultsSetPagination


class TokenObtainPairWithCaptchaView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(request_body=TokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        # if request.recaptcha_result['success']:
        return super().post(request, *args, **kwargs)
        # raise InvalidCaptcha(request.recaptcha_result['message'].replace('\n', ''))


class HealthView(APIView):

    # especifica autenticacion y permisos
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    SERVICE_UNAVAILABLE = 'SERVICE UNAVAILABLE'
    SERVICE_OK = 'SERVICE OK'

    @swagger_auto_schema(responses={
        200: openapi.Response(
            "Service OK",
            HealthSerializer),
        503: openapi.Response(
            "Service UNAVAILABLE",
            HealthSerializer), })
    def get(self, request):
        """
        service health (readiness probe)
        """

        body = HealthSerializer(data={
            'hostname': settings.HOSTNAME,
            'product_name': settings.PRODUCT_SHORT_NAME,
            'product_version': settings.PRODUCT_VERSION,
            'message': self.SERVICE_OK
        })

        response_status = status.HTTP_200_OK
        try:
            healthy()
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception('%s: %s', self.__class__.__name__, str(exc))
            body.initial_data['message'] = self.SERVICE_UNAVAILABLE
            response_status = status.HTTP_503_SERVICE_UNAVAILABLE

        body.is_valid()
        return Response(body.data,
                        status=response_status)
