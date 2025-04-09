from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    # login, cadastro e logOut no sistema
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('inicio/', views.inicio, name='inicio'),
    path('login/', views.sair, name='sair'),
]
