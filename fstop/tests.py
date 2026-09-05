from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

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
        
        return self.username
        
class JWTTests(FstopTestCase):
    def test_get_jwt(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post('/api/token/', data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Invalid username and password returns a 401

# Request to endpoint without JWT returns a 401

# Request to endpoint with JWT returns a 200/201

# Create, list, retrieve, update, delete for each resource, validate missing data

# If user not authenticated to access resource API should return a 401


