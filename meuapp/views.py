from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Servidor, ServidorPreCadastrado
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from django.http import HttpResponse

def index(request):
    return render(request, 'meuapp/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Email recebido: {email}")  # Log de depuração
        print(f"Senha recebida: {password}")  # Log de depuração

        if not email or not password:
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, 'meuapp/login.html')

        user = authenticate(request, username=email, password=password)
        
        # Validação básica dos campos
        if not email or not password:
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, 'meuapp/login.html')

        if user is not None:
            print(f"Usuário autenticado: {user}")  # Log de depuração
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

@login_required
def dashboard(request):
    usuario = request.user  # Obtém o usuário logado

    if hasattr(usuario, "_wrapped"):  # Caso seja um SimpleLazyObject
        usuario = usuario._wrapped

    if not hasattr(usuario, "id") or not isinstance(usuario, Servidor):  # Verifica se o usuário é um Servidor
        print("Usuário não é um Servidor. Tipo real:", type(usuario))
        return HttpResponse("Erro: usuário inválido", status=400)

    if request.method == 'POST':
        form = ReservaForm(request.POST, user=usuario)  # Passa o servidor

        print("Dados recebidos no formulário:", request.POST)  

        if form.is_valid():
            print("Formulário válido. Salvando...")
            reserva = form.save()  # Salva com o servidor definido
            print("Reserva salva com sucesso:", reserva)
            return redirect('dashboard')
        else:
            print("Erro no formulário:", form.errors)  
    else:
        form = ReservaForm(user=usuario)  

    return render(request, 'meuapp/dashboard.html', {'form': form})

def cadastro(request):
    if request.method == 'POST':
        siape = request.POST.get('siape')
        cpf = request.POST.get('cpf')
        
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

        # Verificar se o SIAPE e CPF estão pré-cadastrados
        if ServidorPreCadastrado.objects.filter(siape=siape, cpf=cpf).exists():
            servidor.status = 'aprovado' # Aprova o cadastro do servidor
            servidor.save() # Atualiza o status do servidor

        messages.success(request, "Cadastro realizado com sucesso! Aguarde aprovação.")
        return redirect('aguardo_aprovacao')  # Redireciona para tela de aprovação

    return render(request, 'meuapp/cadastro.html')

def aguardo_aprovacao(request):
    return render(request, 'meuapp/aguardo_aprovacao.html')

def minhas_reservas(request): 
    return render(request, 'meuapp/minhas_reservas.html')
