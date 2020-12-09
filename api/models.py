from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default="user")
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.email
