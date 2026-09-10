from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Client

# Create your tests here.

class FstopTestCase(APITestCase):
    """Contains a method that creates a user for all tests

    Args:
        APITestCase (TestCase): Provides methods for testing Django REST API views
    """
    def setUp(self):
        self.username = 'billythephotog'
        self.password = 'shutterspeed'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

class JWTTests(FstopTestCase):
    """Tests for JWT authentication"""
    def test_get_jwt(self): # Grabs the username and password from the setUp method
        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post( # Sends a post request to /api/token/
            '/api/token/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class InvalidLoginTests(FstopTestCase):
    """
    Tests for invalid login attempts
    """
    def test_invalid_credentials_return_401(self):
        data = {
            'username': 'joe', # This user hasn't signed up, so login should fail
            'password': 'moon'
        }

        response = self.client.post(
            '/api/token/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class AuthenticationRequiredTests(FstopTestCase):
    """ 
    Tests to ensure that only authenticated users can access the clients endpoint
    """
    def test_unauthenticated_user_cannot_access_clients(self):
        response = self.client.get('/api/clients/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationTests(FstopTestCase):
    """
    Tests to ensure that users can only access their own clients
    """
    def test_user_cannot_access_another_users_client(self):
        other_user = User.objects.create_user( # Creates a new user
            username='alice',
            password='password123'
        )

        jane_doe = Client.objects.create( # Creates a new client
            user=other_user,
            first_name='Jane',
            last_name='Doe',
            city='Cleveland',
            state='OH',
            zip_code='44122',
            email='jane@example.com',
            phone_number='+12161234567'
        )

        self.client.force_authenticate(user=self.user) 

        response = self.client.get(
            f'/api/clients/{jane_doe.id}/' # Send a GET request to /client/{id}/ endpoint
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class AuthorizationModificationTests(FstopTestCase):
    """
    Tests that users can't modify other users if they didn't create them
    """
    def test_user_cannot_modify_another_users_client(self):
        other_user = User.objects.create_user(
            username='alice',
            password='password123'
        )

        other_client = Client.objects.create(
            user=other_user,
            first_name='Jane',
            last_name='Doe',
            city='Cleveland',
            state='OH',
            zip_code='44122',
            email='jane@example.com',
            phone_number='+12161234567'
        )

        self.client.force_authenticate(user=self.user)

        data = {
            'first_name': 'Kelly'
        }

        response = self.client.patch(
            f'/api/clients/{other_client.id}/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )