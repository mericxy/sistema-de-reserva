from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

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
