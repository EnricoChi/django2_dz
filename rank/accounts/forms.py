import random
import hashlib

from django import forms

from .models import Account


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'password']

    def save(self, **kwargs):
        user = super().save()
        user.is_active = False

        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user
