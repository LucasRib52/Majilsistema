from django.contrib import admin
from .models import Condominio, PagamentoCondominio

@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_unidade')

@admin.register(PagamentoCondominio)
class PagamentoCondominioAdmin(admin.ModelAdmin):
    list_display = ('condominio', 'valor', 'data_pagamento')
