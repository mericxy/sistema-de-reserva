from django.shortcuts import render

def index(request):
    return render(request, 'meuapp/index.html')

def login(request):
    return render(request, 'meuapp/login.html')

def cadastro(request):
    return render(request, 'meuapp/cadastro.html')

def aguardo_aprovacao(request):
    return render(request, 'meuapp/aguardo_aprovacao.html')