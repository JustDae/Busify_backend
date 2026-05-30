# transit/tests/test_rutas.py
from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client, create_ruta


class RutaPermissionTests(TestCase):

    def setUp(self):
        self.user = create_user('pasajero')
        self.staff = create_staff()
        self.ruta = create_ruta()

    def test_authenticated_user_can_list_rutas(self):
        resp = auth_client(self.user).get('/api/rutas/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_create_ruta(self):
        resp = auth_client(self.user).post('/api/rutas/', {
            'name': 'Quito-Manta', 'origin': 'Quito', 'destination': 'Manta', 'base_fare': 18.00
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_ruta(self):
        resp = auth_client(self.staff).post('/api/rutas/', {
            'name': 'Quito-Manta', 'origin': 'Quito', 'destination': 'Manta', 'base_fare': 18.00, 'is_active': True
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class RutaFilterAndStatsTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('analista'))
        create_ruta(name='Quito-Gye', origin='Quito', destination='Guayaquil', is_active=True)
        create_ruta(name='Quito-Cuenca', origin='Quito', destination='Cuenca', is_active=False)

    def test_filter_by_active_rutas(self):
        resp = self.client.get('/api/rutas/?is_active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_stats_returns_expected_fields(self):
        resp = self.client.get('/api/rutas/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'active', 'inactive']:
            self.assertIn(field, resp.data)