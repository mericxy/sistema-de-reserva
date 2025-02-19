from django.urls import path
from meuapp.views import index, login_view, logout_view, cadastro, aguardo_aprovacao, dashboard

urlpatterns = [
    path('', index, name='index'),
    path('login_view/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('aguardo_aprovacao/', aguardo_aprovacao, name='aguardo_aprovacao'),
    path('dashboard/', dashboard, name='dashboard'),
]
