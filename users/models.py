from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
   

    email = models.EmailField(unique=True)  # make email unique for login
    role = models.CharField(
        max_length=20,
        choices=[("cedant", "Cedant"), ("reinsurer", "Reinsurer"), ("admin", "Admin")],
        default="cedant",
        blank=False
    )
    phone_number = models.CharField(max_length=20, blank=False, null=True)

    def __str__(self):
        return self.username