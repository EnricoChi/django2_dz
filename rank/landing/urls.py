from django.urls import path
from django.views.decorators.cache import cache_page

from .views import LandView

app_name = 'landing'

urlpatterns = [
    path('', LandView.as_view(), name='landing')
    # path('', cache_page(3600)(LandView.as_view()), name='landing')
]
