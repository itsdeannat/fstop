from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Client, Project, Booking, Gallery
from rest_framework.test import force_authenticate

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
    def test_get_jwt(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class InvalidLoginTests(FstopTestCase):
    def test_invalid_credentials_return_401(self):
        data = {'username': 'joe', 'password': 'moon'}
        response = self.client.post('/api/token/', data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class CreateClientTests(FstopTestCase): # Create a client
    def test_create_client(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'city': 'Cincinnati',
            'state': 'OH',
            'zip_code': '45202',
            'email': 'alice.johnson@example.com',
            'phone_number': '+12161239999'
        }
        self.client.force_authenticate(user=self.user) # Authenticate as Billy
        response = self.client.post('/api/clients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateProjectTests(FstopTestCase):
    def test_create_project(self):
        client = Client.objects.create(
            user=self.user,
            first_name='Alice',
            last_name='Johnson',
            city='Cincinnati',
            state='OH',
            zip_code='45202',
            email='alice.johnson@example.com',
            phone_number='+12161239999'
        )
        data = {
            'project_name': 'Birthday Party',
            'project_type': 'party',
            'client_id': str(client.id)
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateBookingTests(FstopTestCase):
    def test_create_booking(self):
        client = Client.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            city='Cleveland',
            state='OH',
            zip_code='44122',
            email='john.doe@example.com',
            phone_number='+12161231234'
        )
        project = Project.objects.create(
            project_name='Wedding',
            project_type='event',
            client=client
        )
        data = {
            'project_id': str(project.id),
            'date': '2026-06-15',
            'time': '14:00:00',
            'duration': 480,
            'location': 'Downtown Venue'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateGalleryTests(FstopTestCase):
    def test_create_gallery(self):
        client = Client.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            city='Cleveland',
            state='OH',
            zip_code='44122',
            email='john.doe@example.com',
            phone_number='+12161231234'
        )
        project = Project.objects.create(
            project_name='Wedding',
            project_type='event',
            client=client
        )
        data = {
            'project_id': str(project.id),
            'gallery_name': 'Reception Photos',
            'picture_count': 89,
            'is_visible': True,
            'url': 'https://example.com/galleries/reception'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/galleries/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

            
