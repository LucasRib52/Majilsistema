from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView

urlpatterns = [
    path('clientes/', login_required(ClienteListView.as_view()), name='clientes_list'),
    path('clientes/novo/', login_required(ClienteCreateView.as_view()), name='clientes_create'),
    path('clientes/editar/<int:pk>/', login_required(ClienteUpdateView.as_view()), name='clientes_edit'),
    path('clientes/excluir/<int:pk>/', login_required(ClienteDeleteView.as_view()), name='clientes_delete'),
]
