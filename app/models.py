
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
    

class Reserva(models.Model):
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f'{self.laboratorio} - {self.data} {self.hora_inicio} às {self.hora_fim}'
