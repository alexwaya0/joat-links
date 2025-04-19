# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]

class CustomUser(AbstractUser):
    whatsapp_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=100)
    preferred_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=True)
    online_status = models.BooleanField(default=False)

    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

