from django.urls import path, re_path, include

from .views import SignUp, SignIn, success_page, verify, sign_out

app_name = 'accounts'

urlpatterns = [
    path('sign_up/', SignUp.as_view(), name='sign-up'),
    path('sign_in/', SignIn.as_view(), name='sign-in'),
    path('sign_out/', sign_out, name='sign-out'),
    path('success/', success_page, name='success'),

    # TODO: убрать регулярку
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', verify, name='verify'),
]
