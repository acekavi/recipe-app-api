from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.test.client import FakePayload
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    # Test the users API (Public)
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # test creating user with valid payload successful
        payload = {
            'email': "test@test.com",
            'password': "testpassword",
            'name': "Test name",
        }
        request = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**request.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', request.data)

    def test_user_exists(self):
        # test checking for duplicate users create
        payload = {
            'email': "test@test.com",
            'password': "testpassword123",
            'name': 'Test',
        }

        create_user(**payload)

        request = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # password must be more than 5 charachters
        payload = {
            'email': "test@test.com",
            'password': "pw",
            'name': 'Test',
        }
        request = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # Test the token is created for user
        payload = {
            'email': "test@test.com",
            'password': "pw12345",
        }
        create_user(**payload)
        request = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        # Test that token is not created due to incorrect credentials
        create_user(email='test@test.com', password='test12345')
        payload = {
            'email': 'test@test.com',
            'password': 'fakepass',
        }

        request = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', request.data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        # Test that token is not created if user doesnt exist
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
        }
        request = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', request.data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        # test  that email or password is not entered
        request = self.client.post(
            TOKEN_URL, {'email': 'test@test.com', 'password': ''})

        self.assertNotIn('token', request.data)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
