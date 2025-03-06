from django.contrib import admin
from meuapp.models import Servidor, ServidorPreCadastrado, Reserva

class ServidorAdmin(admin.ModelAdmin):
    list_display = ('siape', 'cpf', 'email', 'telefone', 'status')
    search_fields = ('siape', 'cpf', 'email', 'telefone', 'status')
    list_filter = ('siape', 'cpf', 'email', 'telefone', 'status')
    list_display_links = ('siape', 'cpf')
    list_filter = ('status',)
    list_editable = ('status',)

class ServidorPreCadastradoAdmin(admin.ModelAdmin):
    list_display = ('siape', 'cpf')
    search_fields = ('siape', 'cpf')
    list_filter = ('siape', 'cpf')
    list_display_links = ('siape', 'cpf')

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('servidor', 'data', 'hora_inicio', 'hora_fim')
    search_fields = ('servidor', 'data', 'hora_inicio', 'hora_fim')
    list_filter = ('servidor', 'data', 'hora_inicio', 'hora_fim')
    list_display_links = ('servidor', 'data', 'hora_inicio', 'hora_fim')

admin.site.register(Servidor, ServidorAdmin)
admin.site.register(ServidorPreCadastrado, ServidorPreCadastradoAdmin)
admin.site.register(Reserva, ReservaAdmin)
