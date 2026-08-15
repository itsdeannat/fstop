from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Client, Project, Booking, Gallery
from django.contrib.auth.models import User


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


class ClientCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating clients - excludes read-only fields (id, created_at)"""
    first_name = serializers.CharField(max_length=20, help_text="Client's first name")
    last_name = serializers.CharField(max_length=20, help_text="Client's last name")
    city = serializers.CharField(max_length=20, help_text="City where client is located")
    state = serializers.CharField(max_length=2, help_text="State abbreviation (e.g., CA, NY)")
    zip_code = serializers.CharField(max_length=20, help_text="Postal code for client's address")
    email = serializers.EmailField(help_text="Client's email address for contact")
    phone_number = serializers.CharField(help_text="Client's phone number")
    
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'city', 'state', 'zip_code', 'email', 'phone_number']
    
    def validate_email(self, value):
        """Ensure email is unique across all clients"""
        if Client.objects.filter(email=value).exists():
            raise ValidationError("A client with this email already exists.")
        return value
    
    def validate_state(self, value):
        """Ensure state is a valid 2-character code"""
        if len(value) != 2 or not value.isalpha():
            raise ValidationError("State must be a 2-letter abbreviation (e.g., CA, NY).")
        return value.upper()
    
    def validate_phone_number(self, value):
        """Ensure phone number is not empty"""
        if not value or len(value.replace('+', '').replace('-', '').replace(' ', '')) < 10:
            raise ValidationError("Phone number must be at least 10 digits.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the project")
    project_name = serializers.CharField(max_length=20, help_text="Name of the project")
    project_type = serializers.ChoiceField(choices=['event', 'portrait', 'party'], help_text="Type of project (event, portrait, or party)")
    client = ClientSerializer(read_only=True, help_text="Details of the client associated with this project")
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source="client",
        write_only=True,
        help_text="UUID of the client for this project"
    )
    created_at = serializers.DateTimeField(read_only=True, help_text="When the project was created")

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_type', 'client', 'client_id', 'created_at']


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating projects - excludes read-only fields (id, client, created_at)"""
    project_name = serializers.CharField(max_length=20, help_text="Name of the project")
    project_type = serializers.ChoiceField(choices=['event', 'portrait', 'party'], help_text="Type of project (event, portrait, or party)")
    client_id = serializers.UUIDField(help_text="UUID of the client for this project")
    
    class Meta:
        model = Project
        fields = ['project_name', 'project_type', 'client_id']


class BookingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the booking")
    project = ProjectSerializer(read_only=True, help_text="Project associated with this booking")
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source="project",
        write_only=True,
        help_text="UUID of the project for this booking"
    )
    date = serializers.DateField(help_text="Date of the booking")
    time = serializers.TimeField(help_text="Time of the booking")
    duration = serializers.IntegerField(help_text="Booking duration in minutes")
    location = serializers.CharField(max_length=20, help_text="Booking location")
    created_at = serializers.DateTimeField(read_only=True, help_text="When the booking was created")
    
    class Meta:
        model = Booking
        fields = ['id', 'project_id', 'project', 'date', 'time', 'duration', 'location', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings - excludes read-only fields (id, project, created_at)"""
    project_id = serializers.UUIDField(help_text="UUID of the project for this booking")
    date = serializers.DateField(help_text="Date of the booking")
    time = serializers.TimeField(help_text="Time of the booking")
    duration = serializers.IntegerField(help_text="Booking duration in minutes")
    location = serializers.CharField(max_length=20, help_text="Booking location")
    
    class Meta:
        model = Booking
        fields = ['project_id', 'date', 'time', 'duration', 'location']


class GallerySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text="Unique identifier for the gallery")
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source="booking",
        write_only=True,
        help_text="UUID of the booking for this gallery"
    )
    booking = BookingSerializer(read_only=True, help_text="Booking associated with this gallery")
    gallery_name = serializers.CharField(max_length=50, help_text="Name of the gallery")
    picture_count = serializers.IntegerField(help_text="Number of pictures in the gallery")
    is_visible = serializers.BooleanField(help_text="Whether the gallery is publicly visible")
    url = serializers.URLField(help_text="URL link to the gallery")
    created_at = serializers.DateTimeField(read_only=True, help_text="Timestamp when gallery was created")
    
    class Meta:
        model = Gallery
        fields = ['id', 'booking', 'booking_id', 'gallery_name', 'picture_count', 'is_visible', 'url', 'created_at']


class GalleryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating galleries - excludes read-only fields (id, project, created_at)"""
    project_id = serializers.UUIDField(help_text="UUID of the project for this gallery")
    gallery_name = serializers.CharField(max_length=50, help_text="Name of the gallery")
    picture_count = serializers.IntegerField(help_text="Number of pictures in the gallery")
    is_visible = serializers.BooleanField(help_text="Whether the gallery is publicly visible")
    url = serializers.URLField(help_text="URL link to the gallery")
    
    class Meta:
        model = Gallery
        fields = ['project_id', 'gallery_name', 'picture_count', 'is_visible', 'url']


class BadRequestSerializer(serializers.Serializer):
    """Serializer for 400 Bad Request responses"""
    detail = serializers.CharField(default="Invalid JSON in request body")


class UnauthorizedSerializer(serializers.Serializer):
    """Serializer for 401 Unauthorized responses"""
    detail = serializers.CharField(default="Authentication credentials were not provided.")


class NotFoundSerializer(serializers.Serializer):
    """Serializer for 404 Not Found responses"""
    detail = serializers.CharField(default="The requested resource was not found.")