from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email address')
    church = models.CharField(max_length=100, blank=True)
    weekend = models.CharField(max_length=100, blank=True, verbose_name='weekend attended')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = []

"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=email.lower(), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        print('created user', user)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        print('created superuser', user)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)
    church = models.CharField(max_length=255)
    weekend = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    # REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or password as these fields will always be prompted for.
    REQUIRED_FIELDS = ['first_name', 'last_name']
"""
