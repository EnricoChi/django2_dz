from datetime import timedelta

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    # TODO: переделать на коробочный django
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

    def __unicode__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class AccountInfo(models.Model):
    GENDER = ((0, ''),
              (1, 'Male'),
              (2, 'Female'))

    account = models.OneToOneField(
        Account, null=False, db_index=True, on_delete=models.CASCADE)
    gender = models.PositiveSmallIntegerField(
        'Gender', choices=GENDER, default=0)
    organization = models.CharField(
        'Organization', max_length=255, blank=True)

    @receiver(post_save, sender=Account)
    def account_info_create(sender, instance, created, **kwargs):
        if created:
            AccountInfo.objects.create(account=instance)

    @receiver(post_save, sender=Account)
    def account_info_save(sender, instance, **kwargs):
        instance.accountinfo.save()
