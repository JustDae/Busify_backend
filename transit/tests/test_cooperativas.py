from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .helpers import create_user, create_staff, auth_client, create_cooperativa


class CooperativaPermissionAndActionsTests(TestCase):

    def setUp(self):
        self.user = create_user('operador')
        self.staff = create_staff()
        self.cooperativa = create_cooperativa(name='Guadalajara', is_active=True)

    def test_unauthenticated_returns_401(self):
        resp = APIClient().get('/api/cooperativas/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_staff_can_register_cooperativa(self):
        resp = auth_client(self.staff).post('/api/cooperativas/', {
            'name': 'Pichincha', 'is_active': True
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)

    def test_regular_user_cannot_register_cooperativa(self):
        resp = auth_client(self.user).post('/api/cooperativas/', {
            'name': 'Pichincha', 'is_active': True
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class CooperativaFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('coordinador'))
        create_cooperativa(name='Compañía Victoria', is_active=True)
        create_cooperativa(name='Termas Turis', is_active=False)

    def test_filter_by_status(self):
        resp = self.client.get('/api/cooperativas/?is_active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['name'], 'Compañía Victoria')