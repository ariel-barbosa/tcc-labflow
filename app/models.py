
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
    TIPO_CHOICES = [
        ('informatica', 'Laboratório de Informática'),
        ('sala_aula', 'Sala de Aula'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    capacidade = models.PositiveIntegerField(blank=True, null=True)
    localizacao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='informatica')
    imagem_url = models.CharField(max_length=255, blank=True, null=True)  # Novo campo para URL da imagem

    def __str__(self):
        return self.nome

    

class Reserva(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.laboratorio} - {self.data} {self.hora_inicio} às {self.hora_fim}'
