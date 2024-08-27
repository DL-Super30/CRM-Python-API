from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserProfile(models.Model):
     username = models.CharField(max_length=255)
     password = models.CharField()
     
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields if necessary


