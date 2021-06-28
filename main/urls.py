from django.urls import path
from .views import create, redirect_to_full_url

urlpatterns = [
    path('create', create, name='create'),
    path('<str:short_url>', redirect_to_full_url, name='redirect'),
]
