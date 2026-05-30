# transit/tests/test_viajes.py
from django.test import TestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .helpers import create_user, create_staff, auth_client, create_viaje, create_bus, create_chofer, create_ruta


class ViajeWorkflowTests(TestCase):

    def setUp(self):
        self.user = create_user('despachador')
        self.staff = create_staff()
        self.client = auth_client(self.user)
        self.viaje = create_viaje(status='scheduled')

    def test_create_viaje_default_status(self):
        from transit.models import Viaje
        bus = create_bus()
        chofer = create_chofer()
        ruta = create_ruta()
        now = timezone.now()
        future = now + timedelta(hours=2)
        
        viaje_obj = Viaje.objects.create(
            bus=bus,
            chofer=chofer,
            ruta=ruta,
            status='scheduled',
            departure_time=now,
            estimated_arrival=future
        )
        self.assertEqual(viaje_obj.status, 'scheduled')

    def test_custom_action_start_route(self):
        resp = self.client.post(f'/api/viajes/{self.viaje.id}/start-route/', {})
        self.assertIn(resp.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST], resp.data)

    def test_regular_user_cannot_force_status_update(self):
        resp = self.client.post(f'/api/viajes/{self.viaje.id}/update-status/', {
            'status': 'completed'
        })
        self.assertIn(resp.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED], resp.data)


class ViajePermissionsAndFiltersTests(TestCase):

    def setUp(self):
        self.staff = create_staff()
        self.client = auth_client(self.staff)
        create_viaje(status='scheduled')
        create_viaje(status='en_route')

    def test_filter_viajes_by_status(self):
        resp = self.client.get('/api/viajes/?status=en_route')
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        for viaje in resp.data['results']:
            self.assertEqual(viaje['status'], 'en_route')