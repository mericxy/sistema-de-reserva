from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from datetime import time, datetime, timedelta

# Classe para gerenciar a criação de usuários
class ServidorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
class ServidorPreCadastrado(models.Model):
    siape = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f"{self.siape} - {self.cpf}"


class Servidor(AbstractUser):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
       
    siape = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aprovado')

    username = None  # Não será utilizado o campo username
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Utiliza o campo email como identificador do usuário
    REQUIRED_FIELDS = ['siape', 'cpf', 'first_name', 'last_name']  # Campos obrigatórios para criação do usuário

    objects = ServidorManager() # Sobrescreve o atributo objects para utilizar o ServidorManager
    
    def clean(self):
        """
        Valida se o SIAPE e CPF existem na tabela ServidorPreCadastrado antes do cadastro.
        A validação só ocorre para novos registros.
        """
        if not self.pk:  # Só valida se for um novo cadastro
            if not ServidorPreCadastrado.objects.filter(siape=self.siape, cpf=self.cpf).exists():
                self.status = 'pendente'    # Se não existir, o status é pendente
            else:
                self.status = 'aprovado'    # Se existir, o status é aprovado

    @property
    def is_active(self):
        """Somente usuários aprovados podem efetuar login"""
        return self.status == 'aprovado'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.siape})"

class Reserva(models.Model):
    AMBIENTE_CHOICES = [
        ('sala', 'Sala'),
        ('laboratorio', 'Laboratório'),
        ('auditorio', 'Auditório'),
    ]

    STATUS_RESERVA_CHOICES = [
        ('aprovada', 'Aprovada'),
        ('pendente', 'Pendente'),
        ('reprovada', 'Reprovada'),
    ]

    servidor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    ambiente_tipo = models.CharField(max_length=20, choices=AMBIENTE_CHOICES)
    ambiente_numero = models.PositiveIntegerField()
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_RESERVA_CHOICES, default='pendente')
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.servidor} em {self.ambiente_tipo} {self.ambiente_numero} ({self.data} {self.hora_inicio}-{self.hora_fim})"

    def clean(self):
        if not self.servidor_id:
            raise ValidationError("O servidor é obrigatório.")
        self.validar_colisao()

    def validar_colisao(self):
        # Verifica se há colisão com outras reservas no mesmo ambiente, dia e horário
        if Reserva.objects.filter(
            ambiente_tipo=self.ambiente_tipo,
            ambiente_numero=self.ambiente_numero,
            data=self.data,
            status__in=['aprovada', 'pendente'],
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio
        ).exclude(id=self.id).exists():
            raise ValidationError("Já existe uma reserva para esse horário.")



    def save(self, *args, **kwargs):
        # Atualiza o status para 'reprovada' se a reserva estiver pendente e a data/horário já passaram
        agora = datetime.now()
        if self.status == 'pendente' and datetime.combine(self.data, self.hora_fim) < agora:
            self.status = 'reprovada'
        super().save(*args, **kwargs)