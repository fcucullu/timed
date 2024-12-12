from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import token_generator


class CustomUser(AbstractUser):
    company = models.CharField(max_length=255, blank=True)
    api_key = models.CharField(max_length=255, unique=True, blank=True) #Created blank, bus assigned by a signal after creation

    def __str__(self):
        return self.username


class AuthenticationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.token
