from django.contrib.auth.base_user import BaseUserManager as DjangoBaseUserManager
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseUserManager(DjangoBaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), blank=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    @classmethod
    def create_user(cls, phone_number, password, first_name='', last_name='', **kwargs):
        try:
            user = cls(phone_number=phone_number, first_name=first_name, last_name=last_name, **kwargs)
            user.set_password(password)
            user.save(using=cls._db)
            return user
        except IntegrityError as error:
            return error

    @classmethod
    def create_superuser(cls, phone_number, password, first_name='', last_name='', **kwargs):
        try:
            kwargs.setdefault('is_staff', True)
            kwargs.setdefault('is_superuser', True)
            return cls.create_user(phone_number, password, first_name, last_name, **kwargs)
        except IntegrityError as error:
            return error


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.name
