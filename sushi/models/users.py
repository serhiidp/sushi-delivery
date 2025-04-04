from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField(blank=True)

    def __str__(self):

        return self.email
