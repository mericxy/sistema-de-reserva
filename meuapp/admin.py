from django.contrib import admin
from meuapp.models import Servidor, ServidorPreCadastrado

class ServidorAdmin(admin.ModelAdmin):
    list_display = ('siape', 'cpf', 'nome', 'email', 'telefone', 'senha')
    search_fields = ('siape', 'cpf', 'nome', 'email', 'telefone', 'senha')
    list_filter = ('siape', 'cpf', 'nome', 'email', 'telefone', 'senha')

class ServidorPreCadastradoAdmin(admin.ModelAdmin):
    list_display = ('siape', 'cpf')
    search_fields = ('siape', 'cpf')
    list_filter = ('siape', 'cpf')

admin.site.register(Servidor, ServidorAdmin)
admin.site.register(ServidorPreCadastrado, ServidorPreCadastradoAdmin)
