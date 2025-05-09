from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('comum', 'Usuário Comum'),
    ]
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default='comum'
    )
    
    # Adicione esses campos para resolver os conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set",  # Nome personalizado
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set",  # Nome personalizado
        related_query_name="usuario",
    )


class Laboratorio(models.Model):
    TIPO_CHOICES = [
        ('informatica', 'Laboratório de Informática'),
        ('eletronica', 'Laboratório de Eletrônica'),
        ('sala_aula', 'Sala de Aula'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome do Laboratório")
    numero = models.IntegerField(verbose_name="Número")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        verbose_name = "Laboratório"
        verbose_name_plural = "Laboratórios"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    numero = models.IntegerField()
    patrimonio = models.IntegerField()
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} (Patrimônio: {self.patrimonio})"

class Funcionamento(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    inicio = models.DateField()
    final = models.DateField()

    def __str__(self):
        return f"Funcionamento de {self.inicio} a {self.final}"


class Reserva(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    motivo = models.TextField()
    
    def clean(self):
        conflitos = Reserva.objects.filter(
            laboratorio=self.laboratorio,
            data=self.data,
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio
        ).exclude(pk=self.pk)
        
        if conflitos.exists():
            raise ValidationError("Já existe uma reserva neste horário")
    
    def __str__(self):
        return f"{self.laboratorio.nome} - {self.data} {self.hora_inicio}-{self.hora_fim}"