from django.test import TestCase

class SimpleTest(TestCase):
    def test_startup(self):
        self.assertEqual(1, 1)