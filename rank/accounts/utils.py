from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_verify_mail(user):
    verify_link = reverse('accounts:verify', args=[user.email, user.activation_key])
    title = f'Account {user.first_name} verification'
    message = f'Account {user.first_name} verification link on site {settings.DOMAIN_NAME}. ' \
              f'Click here: {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
