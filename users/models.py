from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=False,
        blank=False,
        null=False,
        help_text=_("Required. Display name shown to others."),
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("email address"),
        help_text=_("Required. Used for login and verification."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email or f"User {self.pk}"