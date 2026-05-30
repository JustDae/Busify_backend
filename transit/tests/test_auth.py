# transit/tests/test_auth.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .helpers import create_user, get_tokens


class RegisterTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url    = '/api/auth/register/'
        self.data   = {
            'username':  'dae',
            'email':     'dae@test.com',
            'password':  'Pass1234!',
            'password2': 'Pass1234!',
        }

    def test_register_returns_jwt(self):
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('access',   resp.data)
        self.assertIn('refresh',  resp.data)
        self.assertIn('is_staff', resp.data)

    def test_register_passwords_do_not_match(self):
        self.data['password2'] = 'Different!'
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        create_user('dae')
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user   = create_user('martin', password='Pass1234!')

    def test_login_returns_tokens(self):
        resp = self.client.post('/api/auth/login/', {
            'username': 'martin', 'password': 'Pass1234!'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access',   resp.data)
        self.assertIn('refresh',  resp.data)


class RefreshLogoutTests(TestCase):

    def setUp(self):
        self.client  = APIClient()
        self.user    = create_user('tester')
        self.access, self.refresh = get_tokens(self.user)

    def test_logout_blacklists_refresh(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        resp = self.client.post('/api/auth/logout/', {'refresh': self.refresh})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp2 = self.client.post('/api/auth/token/refresh/', {'refresh': self.refresh})
        self.assertEqual(resp2.status_code, status.HTTP_401_UNAUTHORIZED)