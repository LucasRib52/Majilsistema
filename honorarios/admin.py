from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Honorario

@admin.register(Honorario)
class HonorarioAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'valor_total', 'valor_pago', 'data_vencimento', 'status_pagamento', 'data_criacao')
    list_filter = ('status_pagamento', 'data_vencimento')
    search_fields = ('cliente__nome_empresa',)
    ordering = ('-data_vencimento',)
    date_hierarchy = 'data_vencimento'
    list_editable = ('status_pagamento', 'valor_pago')
    readonly_fields = ('data_criacao',)

    fieldsets = (
        ("Dados do Honorário", {
            'fields': ('cliente', 'valor_total', 'valor_pago', 'data_vencimento', 'status_pagamento')
        }),
        ("Informações Adicionais", {
            'fields': ('data_criacao', 'comprovante'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """ Atualiza automaticamente o status do pagamento ao salvar """
        if obj.valor_pago >= obj.valor_total:
            obj.status_pagamento = 'pago'
        else:
            obj.status_pagamento = 'pendente'
        super().save_model(request, obj, form, change)

    # ✅ Botão personalizado para Relatório Financeiro no Admin
    def relatorio_financeiro_link(self, obj=None):
        url = reverse('relatorio_financeiro')  # Usa o nome correto da URL existente
        return format_html(f'<a class="button" href="{url}" target="_blank">📊 Visualizar Relatórios</a>')
    
    relatorio_financeiro_link.short_description = "Relatórios"

    # ✅ Adicionando o botão na interface do admin
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['relatorio_financeiro_link'] = self.relatorio_financeiro_link()
        return super().changelist_view(request, extra_context=extra_context)
