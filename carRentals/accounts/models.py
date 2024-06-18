from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Add email as a required field
    
    def __str__(self):
        return self.username

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset request for {self.user.username}"
