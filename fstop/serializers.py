from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project, Booking, Gallery

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'city', 'state', 'zip_code', 'email', 'phone_number', 'created_at']
    
class ProjectSerializer(serializers.ModelSerializer):
    
    client = ClientSerializer(read_only=True) # Nesting the data here
    client_id = serializers.UUIDField(write_only=True) # So users have to pass the client ID when creating a project
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_type', 'client', 'client_id', 'created_at']
        
class BookingSerializer(serializers.ModelSerializer):
    
    project = ProjectSerializer(read_only=True)
    project_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'project', 'project_id', 'date', 'time', 'duration', 'location', 'created_at']

class GallerySerializer(serializers.ModelSerializer):
    
    project = ProjectSerializer(read_only=True)
    project_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Gallery
        fields = ['id', 'project', 'project_id', 'gallery_name', 'picture_count', 'is_visible', 'url', 'created_at']