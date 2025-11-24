from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model that authenticates with email and stores additional profile data.
    """

    username = None
    email = models.EmailField("email address", unique=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

