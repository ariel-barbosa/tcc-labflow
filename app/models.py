
from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[('admin', 'Administrador'), ('comum', 'Comum')],
        default='comum'
    )

    def __str__(self):
        return self.usuario



class Laboratorio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    capacidade = models.PositiveIntegerField()
    localizacao = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome
