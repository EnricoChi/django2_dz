from django.urls import path

from .views import CompanyView

app_name = 'company'

urlpatterns = [
    path('view/<int:pk>', CompanyView.as_view(), name='view'),
]
