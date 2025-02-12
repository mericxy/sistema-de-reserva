from django.urls import path
from meuapp.views import index, login, cadastro, aguardo_aprovacao

urlpatterns = [
    path('', index),
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('aguardo_aprovacao/', aguardo_aprovacao, name='aguardo_aprovacao'),
]