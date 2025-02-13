from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    CondominioCreateView, CondominioListView, CondominioUpdateView, CondominioDeleteView,
    PagamentoCreateView, PagamentoListView, PagamentoUpdateView, PagamentoDeleteView
)

urlpatterns = [
    # Condomínio
    path('condominio/cadastrar/', login_required(CondominioCreateView.as_view()), name='cadastrar-condominio'),
    path('condominio/listar/', login_required(CondominioListView.as_view()), name='lista-condominios'),
    path('condominio/editar/<int:pk>/', login_required(CondominioUpdateView.as_view()), name='editar-condominio'),
    path('condominio/deletar/<int:pk>/', login_required(CondominioDeleteView.as_view()), name='deletar-condominio'),

    # Pagamento
    path('pagamento/cadastrar/', login_required(PagamentoCreateView.as_view()), name='cadastrar-pagamento'),
    path('pagamento/listar/', login_required(PagamentoListView.as_view()), name='lista-pagamentos'),
    path('pagamento/editar/<int:pk>/', login_required(PagamentoUpdateView.as_view()), name='editar-pagamento'),
    path('pagamento/deletar/<int:pk>/', login_required(PagamentoDeleteView.as_view()), name='deletar-pagamento'),
]
