import random
import hashlib

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from .models import Account, AccountInfo
from .utils import send_verify_mail


class CommonAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class SignUpForm(CommonAccountForm, UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'first_name')

    def save(self, **kwargs):
        user = super().save()

        # TODO: протестить, возможно это вообще не нужно. И убрать из pipeline
        user.is_active = False

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


class AccountEditForm(CommonAccountForm, forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name',)


class AccountInfoEditForm(CommonAccountForm, forms.ModelForm):
    class Meta:
        model = AccountInfo
        fields = ('gender', 'organization')
