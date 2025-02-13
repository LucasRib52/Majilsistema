from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Condominio, PagamentoCondominio
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CondominioForm, PagamentoCondominioForm

# Cadastrar Condomínio
class CondominioCreateView(LoginRequiredMixin, CreateView):
    model = Condominio
    form_class = CondominioForm
    template_name = 'cadastro_condominio.html'
    success_url = reverse_lazy('lista-condominios')

# Listar Condomínios
class CondominioListView(LoginRequiredMixin, ListView):
    model = Condominio
    template_name = 'lista_condominios.html'
    context_object_name = 'condominios'
    paginate_by = 10

# Atualizar Condomínio
class CondominioUpdateView(LoginRequiredMixin, UpdateView):
    model = Condominio
    form_class = CondominioForm
    template_name = 'cadastro_condominio.html'
    success_url = reverse_lazy('lista-condominios')

# Deletar Condomínio
class CondominioDeleteView(LoginRequiredMixin, DeleteView):
    model = Condominio
    template_name = 'confirmar_exclusao.html'
    success_url = reverse_lazy('lista-condominios')

# Cadastrar Pagamento
class PagamentoCreateView(LoginRequiredMixin, CreateView):
    model = PagamentoCondominio
    form_class = PagamentoCondominioForm
    template_name = 'cadastro_pagamento.html'
    success_url = reverse_lazy('lista-pagamentos')

# Listar Pagamentos
class PagamentoListView(LoginRequiredMixin, ListView):
    model = PagamentoCondominio
    template_name = 'lista_pagamentos.html'
    context_object_name = 'pagamentos'
    paginate_by = 10

# Atualizar Pagamento
class PagamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = PagamentoCondominio
    form_class = PagamentoCondominioForm
    template_name = 'cadastro_pagamento.html'
    success_url = reverse_lazy('lista-pagamentos')

# Deletar Pagamento
class PagamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = PagamentoCondominio
    template_name = 'confirmar_exclusao.html'
    success_url = reverse_lazy('lista-pagamentos')
