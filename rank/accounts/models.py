from datetime import timedelta

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.timezone import now

from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Email', unique=True)
    first_name = models.CharField(
        'Name', max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    activation_key = models.CharField(
        'Activation key', max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        'Key validity',
        default=now() + timedelta(hours=48))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        return True

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
