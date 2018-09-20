from . import views
from django.urls import path

app_name = "basket"

urlpatterns = [
    path('add/', views.basket_add, name='add'),
]
