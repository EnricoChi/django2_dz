from django.urls import path

from .views import LandView

app_name = 'landing'

urlpatterns = [
    path('', LandView.as_view(), name='landing')
]
