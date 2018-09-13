from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from .models import Account
from .forms import SignUpForm


class SignUp(CreateView):
    template_name = 'accounts/sign_up.html'
    model = Account
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('accounts:success')


def success_page(request, email):
    if send_verify_mail(email):
        message = f'Your activation email was sent to you - {email}'
    else:
        message = 'error'
    return render(request, 'accounts/success.html', {'message': message})


def send_verify_mail(user):
    verify_link = reverse('accounts:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} \
    на портале {settings.DOMAIN_NAME} перейдите по ссылке: \
    \n{settings.DOMAIN_NAME}{verify_link}'

    print(f'from: {settings.EMAIL_HOST_USER}, to: {user.email}')
    return send_mail(
            title,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


def verify(request, email, activation_key):
    try:
        user = Account.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print(f'user {user} is activated')
            user.is_active = True
            user.save()
            # auth.login(request, user)

            return render(request, 'accounts/verify.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'accounts/verify.html')

    except Exception as e:
        print(f'error activation user : {e.args}')

    return HttpResponseRedirect(reverse('main'))
