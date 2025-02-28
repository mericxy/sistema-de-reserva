import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")  # setup.settings
django.setup()

from meuapp.models import Servidor

email = "admin@example.com" 
if not Servidor.objects.filter(email=email).exists():
    Servidor.objects.create_superuser(
        email=email, 
        password="admin",  # O campo senha deve ser passado como 'password'
        siape="1234567",  # SIAPE é obrigatório
        cpf="123.456.789-00",  # CPF é obrigatório
        first_name="Administrador",  # Nome deve ser passado como 'first_name'
        last_name="do Sistema",  # Sobrenome deve ser passado como 'last_name'
        telefone="(00) 0000-0000",  # Telefone é opcional, mas pode ser incluído
    )
    print("✅ Superusuário criado com sucesso!")
else:
    print("⚠️ Superusuário já existe.")