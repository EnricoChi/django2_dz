import random
import hashlib
import secrets

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Account
from .utils import send_verify_mail


class CommonAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class SignUpForm(CommonAccountForm, forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['email', 'first_name']

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if not secrets.compare_digest(password, password2):
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, **kwargs):
        user = super().save()
        user.is_active = False
        user.set_password(self.cleaned_data.get("password2"))

        # TODO: переделать на коробочный django
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()

        user.save()
        send_verify_mail(user)

        return user


class SignInForm(CommonAccountForm, AuthenticationForm):
    error_messages = {
        'invalid_login': "Something went wrong!",
        'inactive': "This account is inactive.",
    }
