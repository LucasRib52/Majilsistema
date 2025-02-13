from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    HonorarioCreateView, HonorarioListView, HonorarioUpdateView,
    HonorarioDeleteView, PagamentoHonorarioView, ClienteAutocompleteView,
    DetalhesPagamentoView, RelatorioFinanceiroView  # Importando a nova View de Relatório
)

urlpatterns = [
    path('cadastrar/', login_required(HonorarioCreateView.as_view()), name='cadastrar_honorario'),
    path('historico/', login_required(HonorarioListView.as_view()), name='historico_honorarios'),
    path('editar/<int:pk>/', login_required(HonorarioUpdateView.as_view()), name='editar_honorario'),
    path('excluir/<int:pk>/', login_required(HonorarioDeleteView.as_view()), name='excluir_honorario'),
    path('pagar/<int:pk>/', login_required(PagamentoHonorarioView.as_view()), name='pagar_honorario'),
    path('autocomplete-clientes/', login_required(ClienteAutocompleteView.as_view()), name='autocomplete_clientes'),
    path('detalhes/<int:pk>/', login_required(DetalhesPagamentoView.as_view()), name='detalhes_pagamento'),

    # ✅ Adicionando a rota para a tela de relatório financeiro
    path('relatorio-financeiro/', login_required(RelatorioFinanceiroView.as_view()), name='relatorio_financeiro'),
]
