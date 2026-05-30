# transit/tests/test_buses.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .helpers import create_user, create_staff, auth_client, create_bus


class BusPermissionAndActionsTests(TestCase):

    def setUp(self):
        self.user = create_user('operador')
        self.staff = create_staff()
        self.bus = create_bus(unit_number='C-010', model='Mercedes', status='active')

    def test_unauthenticated_returns_401(self):
        resp = APIClient().get('/api/buses/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_staff_can_register_bus(self):
        resp = auth_client(self.staff).post('/api/buses/', {
            'unit_number': 'C-080', 'plate': 'PCX-9988', 'model': 'Hino', 'capacity': 40, 'status': 'active'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)

    def test_regular_user_cannot_register_bus(self):
        resp = auth_client(self.user).post('/api/buses/', {
            'unit_number': 'C-080', 'plate': 'PCX-9988', 'model': 'Hino', 'capacity': 40, 'status': 'active'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class BusFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('coordinador'))
        create_bus(unit_number='C-001', plate='PBA-0001', model='Hino', status='active')
        create_bus(unit_number='C-002', plate='PBA-0002', model='Toyota', status='inactive')

    def test_filter_by_status(self):
        resp = self.client.get('/api/buses/?status=active')
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['unit_number'], 'C-001')