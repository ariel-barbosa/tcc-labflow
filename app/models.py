from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.usuario

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
    observacao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data', 'hora_inicio']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.laboratorio} - {self.data} {self.hora_inicio} às {self.hora_fim}"

    def clean(self):
        conflitos = Reserva.objects.filter(
            laboratorio=self.laboratorio,
            data=self.data,
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio
        ).exclude(pk=self.pk if self.pk else None)

        if conflitos.exists():
            raise ValidationError("Conflito de horário com reserva existente")

        if timezone.now() > timezone.make_aware(
            timezone.datetime.combine(self.data, self.hora_inicio)
        ):
            raise ValidationError("Não é possível reservar para datas/horários passados")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)