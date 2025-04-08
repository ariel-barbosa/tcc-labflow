from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio')  # Redireciona automaticamente para /login
]