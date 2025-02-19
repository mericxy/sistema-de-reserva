from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Servidor, ServidorPreCadastrado
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'meuapp/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('dashboard')  # Redireciona para a página principal
        else:
            messages.error(request, "Email ou senha inválidos.")

    return render(request, 'meuapp/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')

def dashboard(request):
    return render(request, 'meuapp/dashboard.html')

def cadastro(request):
    if request.method == 'POST':
        siape = request.POST.get('siape')
        cpf = request.POST.get('cpf')

        # Verificar se o SIAPE e CPF estão na tabela ServidorPreCadastrado
        if not ServidorPreCadastrado.objects.filter(siape=siape, cpf=cpf).exists():
            messages.error(request, "SIAPE e CPF não encontrados no sistema. Cadastro não permitido.")
            return redirect('cadastro')
        
        # Verificar se o SIAPE e CPF já estão cadastrados na tabela Servidor
        if Servidor.objects.filter(siape=siape, cpf=cpf).exists():
            messages.error(request, "SIAPE e CPF já cadastrados no sistema.")
            return redirect('cadastro')

        # Obter os dados do formulário
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')

        # Criar e salvar o usuário corretamente
        servidor = Servidor(
            siape=siape,
            cpf=cpf,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telefone=telefone,
            status='pendente'  # Novos usuários começam como pendentes
        )
        servidor.set_password(senha)  # Armazena a senha de forma segura
        servidor.save()

        messages.success(request, "Cadastro realizado com sucesso! Aguarde aprovação.")
        return redirect('aguardo_aprovacao')  # Redireciona para tela de aprovação

    return render(request, 'meuapp/cadastro.html')

def aguardo_aprovacao(request):
    return render(request, 'meuapp/aguardo_aprovacao.html')
