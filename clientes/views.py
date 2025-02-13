from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import render
from .models import Cliente
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ClienteForm

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes_list.html'
    context_object_name = 'clientes'
    ordering = ['nome_empresa']  # Ordenação alfabética (A-Z)
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(Q(nome_empresa__icontains=search_query))

        return queryset



class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes_form.html'
    success_url = reverse_lazy('clientes_list')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes_form.html'
    success_url = reverse_lazy('clientes_list')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes_confirm_delete.html'
    success_url = reverse_lazy('clientes_list')
