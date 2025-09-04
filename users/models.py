from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staff_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self.create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):

    objects = UserManager()

    email =  models.EmailField(unique=True, verbose_name="Email Adress")
    username = models.CharField(max_length=45, unique = False, verbose_name="Username")
    password = models.CharField(verbose_name="Password")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    @property
    def display_name(self):
        return f"{self.username}#{self.id}"


    def __str__(self):
        return self.email or f"User {self.pk}"

    @classmethod
    def find_by_email(cls, email):
        return cls.objects.filter(email__iexact = email).first()
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower
        super().save(*args, **kwargs)
        

