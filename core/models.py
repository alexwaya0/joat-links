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


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

