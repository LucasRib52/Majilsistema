from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_empresa', 'tipo_pessoa', 'cnpj', 'cpf', 'data_cadastro')
    search_fields = ('nome_empresa', 'cnpj', 'cpf')
    list_filter = ('tipo_pessoa', 'data_cadastro')
    ordering = ('-data_cadastro',)

admin.site.register(Cliente, ClienteAdmin)
