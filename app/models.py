
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


from django.db import models

class Laboratorio(models.Model):
    TIPO_CHOICES = [
        ('informatica', 'Laboratório de Informática'),
        ('eletronica', 'Laboratório de Eletrônica'),
        ('sala_aula', 'Sala de Aula'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome do Laboratório")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='informatica')
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    capacidade = models.PositiveIntegerField(verbose_name="Capacidade de Pessoas")
    localizacao = models.CharField(max_length=100, verbose_name="Localização")
    imagem = models.ImageField(upload_to='laboratorios/', blank=True, null=True, verbose_name="Foto do Laboratório")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível para Reserva")

    class Meta:
        verbose_name = "Laboratório"
        verbose_name_plural = "Laboratórios"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    

from django.core.exceptions import ValidationError
from django.utils import timezone

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
        # Verifica conflitos de horário
        conflitos = Reserva.objects.filter(
            laboratorio=self.laboratorio,
            data=self.data,
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio
        ).exclude(pk=self.pk if self.pk else None)

        if conflitos.exists():
            raise ValidationError("Já existe uma reserva para este laboratório no horário selecionado")

        # Verifica se a data/hora é futura
        if timezone.now() > timezone.make_aware(
            timezone.datetime.combine(self.data, self.hora_inicio)
        ):
            raise ValidationError("Não é possível reservar para datas/horários passados")

    def save(self, *args, **kwargs):
        self.full_clean()  # Executa as validações
        super().save(*args, **kwargs)
