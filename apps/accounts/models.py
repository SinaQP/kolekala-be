from django.contrib.auth.base_user import BaseUserManager as DjangoBaseUserManager
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.core.models import Model


class BaseUserManager(DjangoBaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    @classmethod
    def create_user(cls, email, password, **kwargs):
        try:
            user = cls(email=email, **kwargs)
            user.set_password(password)
            user.save()
            return user
        except IntegrityError as error:
            return error

    @classmethod
    def create_superuser(cls, email, password, **kwargs):
        try:
            kwargs.setdefault('is_staff', True)
            kwargs.setdefault('is_superuser', True)
            return cls.create_user(email, password, **kwargs)
        except IntegrityError as error:
            return error


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.name
