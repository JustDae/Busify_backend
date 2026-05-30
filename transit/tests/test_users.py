# transit/tests/test_users.py
from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client


class UserProfileTests(TestCase):

    def setUp(self):
        self.user = create_user('romina')
        self.client = auth_client(self.user)

    def test_get_own_profile(self):
        resp = self.client.get('/api/users/profile/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], 'romina')


class UserStaffManagementTests(TestCase):

    def setUp(self):
        self.staff = create_staff()
        self.user = create_user('chofer_nuevo')

    def test_regular_user_cannot_list_system_users(self):
        resp = auth_client(self.user).get('/api/users/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_list_users_and_see_stats(self):
        client_staff = auth_client(self.staff)
        resp = client_staff.get('/api/users/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        resp_stats = client_staff.get('/api/users/stats/')
        self.assertEqual(resp_stats.status_code, status.HTTP_200_OK)
        self.assertIn('total', resp_stats.data)