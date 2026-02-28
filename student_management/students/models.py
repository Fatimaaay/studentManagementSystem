from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



# Student Model
class Student(models.Model):
    # Each field is a column in the database
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=50)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-enrollment_date']  # Newest first


import uuid
from django.utils import timezone
from datetime import timedelta


# UserProfile for email verification
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    token_created_at = models.DateTimeField(auto_now_add=True)

    def is_token_valid(self):
        # Token expires after 24 hours
        expiry_time = self.token_created_at + timedelta(hours=24)
        return timezone.now() < expiry_time

    def __str__(self):
        return f"{self.user.username} - Verified: {self.email_verified}"