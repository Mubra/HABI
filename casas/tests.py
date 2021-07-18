'''
Pruebas unitarias aplicacion SRSI
'''
from unittest.mock import call, patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from casas import views
from casas.serializers import HealthSerializer

User = get_user_model()


class PrintDocTestCase(TestCase):
    '''
    Extiende la Clase TestCase
    imprime docstrings de clase y metodo
    '''

    def __call__(self, result=None):
        test_method = getattr(self, self._testMethodName)

        cls_doc = self.__class__.__doc__.strip().upper()
        test_method_doc = test_method.__doc__
        tab = ' '*4
        print('\n' + tab + cls_doc)
        print(tab + 'Caso de Prueba:')
        print(tab * 2 + test_method_doc)
        return super().__call__(result=result)


class HealthViewTest(PrintDocTestCase):
    '''
    casos de Prueba del endpoint de salud del servicio
    '''

    @patch('srsi_app.views.healthy')
    def test_health_view_service_ok(self, mock_healthy):
        '''
        endpoint de salud responde SERVICE OK
        '''
        client = APIClient()

        resp = client.get(reverse('health'))

        calls = [call()]
        self.assertEqual(calls, mock_healthy.mock_calls)

        self.assertEqual(resp.status_code, 200, 'status code 200 is expected')

        serializer = HealthSerializer(data=resp.json())
        self.assertTrue(serializer.is_valid(raise_exception=False),
                        'response must be valid HealthSerializer data')

        self.assertEqual(serializer.data['message'],
                         views.HealthView.SERVICE_OK)

    @patch('casas.views.healthy')
    @patch('casas.views.logger')
    def test_health_view_service_unavailable(self, mock_logger,
                                             mock_healthy):
        '''
        endpoint salud, responde SERVICE_UNAVAILABLE
        (cuando la funcion healthy levanta una excepcion)
        '''
        # healthy() levanta una excepcion
        mock_healthy.side_effect = Exception()

        client = APIClient()

        resp = client.get(reverse('health'))

        calls = [call()]
        self.assertEqual(calls, mock_healthy.mock_calls)

        logger_calls = [call.exception(
            '%s: %s', views.HealthView().__class__.__name__, '')]
        self.assertEqual(logger_calls, mock_logger.mock_calls)

        self.assertEqual(resp.status_code, 503, 'status code 503 is expected')

        serializer = HealthSerializer(data=resp.json())
        self.assertTrue(serializer.is_valid(raise_exception=False),
                        'response must be valid HealthSerializer data')

        self.assertEqual(serializer.data['message'],
                         views.HealthView.SERVICE_UNAVAILABLE)

# pylint: disable=too-many-instance-attributes
