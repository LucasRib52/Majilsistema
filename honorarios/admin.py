from django.contrib import admin
from .models import Honorario

@admin.register(Honorario)
class HonorarioAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'valor_total', 'valor_pago', 'data_vencimento', 'status_pagamento', 'data_criacao')
    list_filter = ('status_pagamento', 'data_vencimento')
    search_fields = ('cliente__nome_empresa',)
    ordering = ('-data_vencimento',)
    date_hierarchy = 'data_vencimento'

    # ✅ Campos editáveis diretamente na listagem
    list_editable = ('status_pagamento', 'valor_pago')

    # ✅ Campos somente leitura no painel de edição
    readonly_fields = ('data_criacao',)

    # ✅ Personalizando a exibição do formulário no Django Admin
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
