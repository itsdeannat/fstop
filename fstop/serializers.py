from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project, Booking, Gallery

class ClientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the client")
    first_name = serializers.CharField(max_length=20, help_text="Client's first name")
    last_name = serializers.CharField(max_length=20, help_text="Client's last name")
    city = serializers.CharField(max_length=20, help_text="City where client is located")
    state = serializers.CharField(max_length=2, help_text="State abbreviation (e.g., CA, NY)")
    zip_code = serializers.CharField(max_length=20, help_text="Postal code for client's address")
    email = serializers.EmailField(help_text="Client's email address for contact")
    phone_number = serializers.CharField(help_text="Client's phone number")
    created_at = serializers.DateTimeField(read_only=True, help_text="Timestamp when client was created")
    
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'city', 'state', 'zip_code', 'email', 'phone_number', 'created_at']
    
class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the project")
    project_name = serializers.CharField(max_length=20, help_text="Name of the project")
    project_type = serializers.ChoiceField(choices=['event', 'portrait', 'party'], help_text="Type of project (event, portrait, or party)")
    client = ClientSerializer(read_only=True, help_text="Client associated with this project")
    client_id = serializers.UUIDField(write_only=True, help_text="UUID of the client for this project")
    created_at = serializers.DateTimeField(read_only=True, help_text="When the project was created")
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_type', 'client', 'client_id', 'created_at']
        
class BookingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the booking")
    project = ProjectSerializer(read_only=True, help_text="Project associated with this booking")
    project_id = serializers.UUIDField(write_only=True, help_text="UUID of the project for this booking")
    date = serializers.DateField(help_text="Date of the booking")
    time = serializers.TimeField(help_text="Time of the booking")
    duration = serializers.IntegerField(help_text="Booking duration in minutes")
    location = serializers.CharField(max_length=20, help_text="Booking location")
    created_at = serializers.DateTimeField(read_only=True, help_text="When the booking was created")
    
    class Meta:
        model = Booking
        fields = ['id', 'project', 'project_id', 'date', 'time', 'duration', 'location', 'created_at']

class GallerySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the gallery")
    project = ProjectSerializer(read_only=True, help_text="Project associated with this gallery")
    project_id = serializers.UUIDField(write_only=True, help_text="UUID of the project for this gallery")
    gallery_name = serializers.CharField(max_length=50, help_text="Name of the gallery")
    picture_count = serializers.IntegerField(help_text="Number of pictures in the gallery")
    is_visible = serializers.BooleanField(help_text="Whether the gallery is publicly visible")
    url = serializers.URLField(help_text="URL link to the gallery")
    created_at = serializers.DateTimeField(read_only=True, help_text="Timestamp when gallery was created")
    
    class Meta:
        model = Gallery
        fields = ['id', 'project', 'project_id', 'gallery_name', 'picture_count', 'is_visible', 'url', 'created_at']
        
class BadRequestSerializer(serializers.Serializer):
    """Serializer for 400 Bad Request responses"""
    detail = serializers.CharField(default="Invalid JSON in request body")
 
 
class UnauthorizedSerializer(serializers.Serializer):
    """Serializer for 401 Unauthorized responses"""
    detail = serializers.CharField(default="Authentication credentials were not provided.")
 
 
class NotFoundSerializer(serializers.Serializer):
    """Serializer for 404 Not Found responses"""
    detail = serializers.CharField(default="The requested resource was not found.")