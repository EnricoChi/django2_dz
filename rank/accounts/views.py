from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Account, AccountInfo
from .forms import SignUpForm, SignInForm, AccountEditForm, AccountInfoEditForm


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


class AccountEdit(UpdateView):
    model = Account
    form_class = AccountEditForm
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('landing:landing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_info'] = AccountInfoEditForm(self.request.POST or None, instance=self.request.user.accountinfo)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_info = context['form_info']
        if form_info.is_valid():
            form_info.save()
        return super().form_valid(form)


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
        auth.login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')
        message = 'Account successfully activated'
    return render(request, 'accounts/success.html', {'message': message})
