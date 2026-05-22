from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.

class Client(models.Model):
    """
    Model representing a client in the fstop database
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=20, help_text="Client's first name")
    last_name = models.CharField(max_length=20, help_text="Client's last name")
    city = models.CharField(max_length=20, help_text="City where client is located")
    state = models.CharField(max_length=2, help_text="State abbreviation (e.g., CA, NY)")
    zip_code = models.CharField(max_length=20, help_text="Postal code for client's address")
    email = models.EmailField(help_text="Client's email address for contact")
    phone_number = PhoneNumberField(help_text="Client's phone number")
    created_at = models.DateTimeField(auto_now_add=True)
 
class Project(models.Model):
    """
    Model representing a Project in the fstop database
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=20, help_text="Name of the project")
    EVENT = "event"
    PORTRAIT = "portrait"
    PARTY = "party"
    PROJECT_CHOICES = {
        EVENT: "Event",
        PORTRAIT: "Portrait",
        PARTY: "Party",
    }
    project_type = models.CharField(max_length=8, choices=PROJECT_CHOICES, default=EVENT, help_text="Type of project (event, portrait, or party)")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, help_text="Client associated with this project")
    created_at = models.DateTimeField(auto_now_add=True)
 
class Booking(models.Model):
    """
    Model representing a Booking in the fstop database
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="Project associated with this booking")
    date = models.DateField(help_text="Date of the booking")
    time = models.TimeField(help_text="Time of the booking")
    duration = models.IntegerField(help_text="Booking duration in minutes")
    location = models.CharField(max_length=20, help_text="Booking location")
    created_at = models.DateTimeField(auto_now_add=True)
 
class Gallery(models.Model):
    """
    Model representing a Gallery in the fstop database
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="Project associated with this gallery")
    gallery_name = models.CharField(max_length=50, help_text="Name of the gallery")
    picture_count = models.IntegerField(help_text="Number of pictures in the gallery")
    is_visible = models.BooleanField(help_text="Whether the gallery is publicly visible")
    url = models.URLField(help_text="URL link to the gallery")
    created_at = models.DateTimeField(auto_now_add=True)