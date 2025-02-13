from django.db import models
from django.core.exceptions import ValidationError

class ServidorPreCadastrado(models.Model):
    siape = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f"{self.siape} - {self.cpf}"


class Servidor(models.Model):
    siape = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    senha = models.CharField(max_length=128)

    def clean(self):
        """
        Valida se o SIAPE e CPF existem na tabela ServidorPreCadastrado antes do cadastro.
        """
        if not ServidorPreCadastrado.objects.filter(siape=self.siape, cpf=self.cpf).exists():
            raise ValidationError("SIAPE e CPF não encontrados no sistema. Cadastro não permitido.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome if self.nome else f"Servidor {self.siape}"
