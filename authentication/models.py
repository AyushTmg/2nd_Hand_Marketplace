from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    email=models.EmailField(unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']

    def __str__(self) -> str:
        return f"{self.username}"
