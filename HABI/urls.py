"""HABI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from casas.views import TokenObtainPairWithCaptchaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('casas.urls')),

    # simple-jwt
    path('api/token/', TokenObtainPairWithCaptchaView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

SchemaView = get_schema_view(
    openapi.Info(
        title=settings.PRODUCT_SHORT_NAME + " API",
        default_version=f'version: {settings.PRODUCT_VERSION}',
        description=f'{settings.PRODUCT_LONG_NAME} ({settings.PRODUCT_OU})',
        terms_of_service=settings.TERMS_OF_SERVICE_URL,
        contact=openapi.Contact(email=f'{settings.PRODUCT_CONTACT_EMAIL}'),
        license=openapi.License(
            name=F"Propiedad {settings.PRODUCT_AGENCY_DESCRIPTION}"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$',
            SchemaView.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', SchemaView.with_ui(
            'swagger',
            cache_timeout=0),
            name='schema-swagger-ui'),
        url(r'^redoc/$', SchemaView.with_ui(
            'redoc',
            cache_timeout=0),
            name='schema-redoc'),

    ]
