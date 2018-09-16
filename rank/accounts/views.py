from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from .models import Account
from .forms import SignUpForm, SignInForm


class RedirectAuthUserMixin:
    def dispatch(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, **kwargs)


class SignUp(RedirectAuthUserMixin, CreateView):
    template_name = 'accounts/sign_up.html'
    model = Account
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('accounts:success')


class SignIn(LoginView):
    authentication_form = SignInForm
    template_name = "accounts/sign_in.html"
    redirect_authenticated_user = True


def success_page(request):
    message = f'Link to activate your account was sent to your e-mail'
    return render(request, 'accounts/success.html', {'message': message})


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('landing:landing'))


def verify(request, email, activation_key):
    user = get_object_or_404(Account, email=email)
    message = 'Account can not be activated'
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        user.is_active = True
        user.save()
        auth.login(request, user)
        message = 'Account successfully activated'
    return render(request, 'accounts/success.html', {'message': message})
