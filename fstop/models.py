from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.

class Client(models.Model):
    """
    Model representing a client in the fstop database
    
    Attributes:
    

    Args:
        models (_type_): _description_
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Project(models.Model):
    """
    Model representing a Project in the fstop database

    Args:
        models (_type_): _description_
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=20)  
    EVENT = "event"
    PORTRAIT = "portrait"
    PARTY = "party"
    PROJECT_CHOICES = {
       EVENT: "Event",
       PORTRAIT: "Portrait",
       PARTY: "Party",
    }
    project_type = models.CharField(max_length=8, choices=PROJECT_CHOICES, default=EVENT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Booking(models.Model):
    """
    Model representing a Booking in the fstop database

    Args:
        models (_type_): _description_
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    location = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Gallery(models.Model):
    """
    Model representing a Gallery in the fstop database

    Args:
        models (_type_): _description_
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    gallery_name = models.CharField(max_length=50)
    picture_count = models.IntegerField()
    is_visible = models.BooleanField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)