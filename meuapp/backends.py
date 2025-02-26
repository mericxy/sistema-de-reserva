from django.contrib.auth.backends import BaseBackend
from .models import Servidor

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Tentativa de autenticação: {username}")
        try:
            user = Servidor.objects.get(email=username)  # Busca o usuário pelo email
            print(f"Usuário encontrado: {user}")
            if user.check_password(password):  # Verifica a senha
                print("Senha válida")
                return user
            else:
                print("Senha inválida")
        except Servidor.DoesNotExist:
            print("Usuário não encontrado")
            return None  # Retorna None se o usuário não existir

    def get_user(self, user_id):
        try:
            return Servidor.objects.get(pk=user_id)  # Retorna o usuário pelo ID
        except Servidor.DoesNotExist:
            return None  # Retorna None se o usuário não existir