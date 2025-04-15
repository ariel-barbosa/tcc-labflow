from django.db import models

class Usuario(models.Model):
    TIPO_USUARIO = [
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('admin', 'Administrador'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO)

    def __str__(self):
        return f"{self.nome} ({self.tipo_usuario})"


class Laboratorio(models.Model):
    TIPO_LAB = [
        ('mecânica', 'Mecânica'),
        ('informática', 'Informática'),
        ('química', 'Química'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=TIPO_LAB)
    capacidade = models.IntegerField()
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Reserva(models.Model):
    STATUS = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    data_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return f"{self.usuario.nome} - {self.laboratorio.nome} em {self.data_reserva}"


class HistoricoReserva(models.Model):
    STATUS = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('cancelada', 'Cancelada'),
    ]

    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    data_modificacao = models.DateTimeField(auto_now_add=True)
    status_anterior = models.CharField(max_length=10, choices=STATUS)
    status_novo = models.CharField(max_length=10, choices=STATUS)
    usuario_acao = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Histórico da Reserva {self.reserva.id} em {self.data_modificacao}"


class RegraReserva(models.Model):
    descricao = models.TextField()
    valor = models.CharField(max_length=50)
    unidade = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Regra: {self.descricao} - {self.valor} {self.unidade or ''}"
