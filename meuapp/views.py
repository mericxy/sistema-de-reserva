from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Servidor, ServidorPreCadastrado

def index(request):
    return render(request, 'meuapp/index.html')

def login(request):
    return render(request, 'meuapp/login.html')

def cadastro(request):
    if request.method == 'POST':
        siape = request.POST.get('siape')
        cpf = request.POST.get('cpf')

        # Verificar se o SIAPE e o CPF estão na tabela ServidorPreCadastrado
        if not ServidorPreCadastrado.objects.filter(siape=siape, cpf=cpf).exists():
            messages.error(request, "SIAPE e CPF não encontrados no sistema. Cadastro não permitido.")
            return redirect('cadastro')

        # Se a validação for bem-sucedida, criar o novo servidor
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')  # Você pode hash a senha usando set_password antes de salvar

        servidor = Servidor.objects.create(
            siape=siape,
            cpf=cpf,
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha  # Recomenda-se usar set_password() para segurança
        )

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login')
    return render(request, 'meuapp/cadastro.html')

def aguardo_aprovacao(request):
    return render(request, 'meuapp/aguardo_aprovacao.html')