# import the required libraries
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile = models.ImageField(upload_to="profile/doctor/")
    address = models.TextField()
    

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile = models.ImageField(upload_to="profile/patient/")
    address = models.TextField()

