from django.urls import path, re_path

from .views import SignUp, success_page, verify

app_name = 'accounts'

urlpatterns = [
    path('sign_up/', SignUp.as_view(), name='sign-up'),
    path('success/', success_page, name='success'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', verify, name='verify'),
]
