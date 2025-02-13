from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView, View, DetailView, TemplateView
from .models import Honorario
from .forms import HonorarioForm, PagamentoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import HonorarioUpdateForm  # Importando o novo form
from django.db.models import Q
from datetime import datetime
from clientes.models import Cliente
from django.utils.timezone import now
from datetime import date
from collections import defaultdict
from django.db.models import Sum, Count, F
import json



class HonorarioCreateView(LoginRequiredMixin, CreateView):
    model = Honorario
    form_class = HonorarioForm
    template_name = "cadastrar_honorario.html"
    success_url = reverse_lazy('historico_honorarios')

    def form_valid(self, form):
        cliente_id = self.request.POST.get("cliente_id")  # Obtém o ID do cliente enviado no formulário
        
        if not cliente_id:
            form.add_error("cliente_nome", "Cliente não encontrado. Selecione um cliente válido.")
            return self.form_invalid(form)

        try:
            cliente = Cliente.objects.get(id=cliente_id)  # Busca o cliente no banco de dados
        except Cliente.DoesNotExist:
            form.add_error("cliente_nome", "Cliente não encontrado. Selecione um cliente válido.")
            return self.form_invalid(form)

        honorario = form.save(commit=False)
        honorario.cliente = cliente  # Define o cliente no modelo Honorario

        # ✅ Definir data de vencimento automática (dia 10 do mês atual)
        if not honorario.data_vencimento:
            hoje = date.today()
            honorario.data_vencimento = date(hoje.year, hoje.month, 10)

        honorario.save()

        return super().form_valid(form)

class HonorarioListView(LoginRequiredMixin, ListView):
    model = Honorario
    template_name = 'historico_honorarios.html'
    context_object_name = 'honorarios'
    paginate_by = 10

    def get_queryset(self):
        honorarios = Honorario.objects.select_related('cliente')

        # 🔍 Pegando os filtros do request
        hoje = date.today()
        mes = self.request.GET.get('mes', str(hoje.month))  # ✅ Define mês atual por padrão
        ano = self.request.GET.get('ano', str(hoje.year))  # ✅ Define ano atual por padrão
        cliente_nome = self.request.GET.get('cliente', '').strip()
        status = self.request.GET.get('status')
        ordenar = self.request.GET.get('ordenar')

        # ✅ Filtro por mês e ano (se não for escolhido, filtra o atual)
        if mes.isdigit() and ano.isdigit():
            honorarios = honorarios.filter(data_vencimento__year=int(ano), data_vencimento__month=int(mes))

        # ✅ Filtro por nome do cliente
        if cliente_nome:
            honorarios = honorarios.filter(cliente__nome_empresa__icontains=cliente_nome)

        # ✅ Filtro por status de pagamento
        if status in ['pago', 'pendente']:
            honorarios = honorarios.filter(status_pagamento=status)

        # ✅ Ordenação A-Z / Z-A
        if ordenar == 'a-z':
            honorarios = honorarios.order_by('cliente__nome_empresa')
        elif ordenar == 'z-a':
            honorarios = honorarios.order_by('-cliente__nome_empresa')

        # ✅ Adiciona o valor faltante em cada honorário
        for honorario in honorarios:
            honorario.valor_faltante = honorario.valor_total - honorario.valor_pago

        return honorarios

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = date.today()
        context['clientes'] = Cliente.objects.all()
        context['meses'] = range(1, 13)
        context['anos'] = [2025, 2026]  # ✅ Apenas os anos 2025 e 2026
        context['mes_atual'] = str(hoje.month)  # ✅ Passa o mês atual para o template
        context['ano_atual'] = str(hoje.year)  # ✅ Passa o ano atual para o template
        return context
    


class HonorarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Honorario
    form_class = HonorarioUpdateForm
    template_name = "editar_honorario.html"
    success_url = reverse_lazy('historico_honorarios')

    def form_valid(self, form):
        honorario = form.save(commit=False)

        # ✅ Apenas os meses futuros serão atualizados
        Honorario.objects.filter(
            cliente=honorario.cliente,
            data_vencimento__gt=honorario.data_vencimento,  # Garante que apenas os futuros serão alterados
            status_pagamento='pendente'  # Evita modificar os já pagos
        ).update(valor_total=honorario.valor_total)

        return super().form_valid(form)

class HonorarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Honorario
    template_name = "excluir_honorario.html"
    success_url = reverse_lazy('historico_honorarios')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"status": "success"})
        return response

class PagamentoHonorarioView(LoginRequiredMixin, FormView):
    template_name = "pagar_honorario.html"
    form_class = PagamentoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        honorario = get_object_or_404(Honorario, pk=self.kwargs['pk'])
        
        # Calcula o valor faltante
        valor_faltante = honorario.valor_total - honorario.valor_pago
        
        # Adiciona os valores ao contexto
        context['honorario'] = honorario
        context['valor_faltante'] = valor_faltante
        
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['honorario'] = get_object_or_404(Honorario, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        honorario = get_object_or_404(Honorario, pk=self.kwargs['pk'])
        valor_pago = form.cleaned_data['valor_pago']

        # Atualiza o valor já pago
        honorario.valor_pago += valor_pago

        # Verifica se há um comprovante e adiciona ao honorário
        if 'comprovante' in self.request.FILES:
            honorario.comprovante = self.request.FILES['comprovante']
        
        honorario.save()
        return redirect('historico_honorarios')



class ClienteAutocompleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        termo = request.GET.get('q', '').strip()
        clientes = Cliente.objects.filter(
            Q(nome_empresa__icontains=termo) | Q(cnpj__icontains=termo) | Q(cpf__icontains=termo)
        )[:10]  # Limita a 10 resultados

        resultados = [
            {
                "id": cliente.id,
                "nome": cliente.nome_empresa,
                "cnpj_cpf": cliente.cnpj if cliente.tipo_pessoa == "CNPJ" else cliente.cpf
            }
            for cliente in clientes
        ]
        
        return JsonResponse(resultados, safe=False)
    
class DetalhesPagamentoView(LoginRequiredMixin, DetailView):
    model = Honorario
    template_name = "detalhes_pagamento.html"
    context_object_name = 'honorario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        honorario = self.get_object()

        # Adiciona os dados do pagamento ao contexto
        context['data_pagamento'] = honorario.data_criacao
        context['valor_pago'] = honorario.valor_pago
        context['comprovante'] = honorario.comprovante

        return context
    

class RelatorioFinanceiroView(LoginRequiredMixin, TemplateView):
    template_name = "relatorio_financeiro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Lista de anos disponíveis no banco
        anos = Honorario.objects.dates("data_vencimento", "year", order="DESC")
        meses = [
            (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), (4, "Abril"), (5, "Maio"),
            (6, "Junho"), (7, "Julho"), (8, "Agosto"), (9, "Setembro"), (10, "Outubro"),
            (11, "Novembro"), (12, "Dezembro"),
        ]

        # Pegando o mês e ano atuais
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year

        # Pegando filtros da URL
        ano_selecionado = self.request.GET.get("ano")
        mes_selecionado = self.request.GET.get("mes")

        try:
            ano_selecionado = int(ano_selecionado) if ano_selecionado else ano_atual
            mes_selecionado = int(mes_selecionado) if mes_selecionado else mes_atual  # Inicia no mês atual
        except ValueError:
            ano_selecionado = ano_atual
            mes_selecionado = mes_atual

        # Filtrando os honorários pelo ano e mês selecionado
        queryset = Honorario.objects.filter(data_vencimento__year=ano_selecionado)
        if mes_selecionado:
            queryset = queryset.filter(data_vencimento__month=mes_selecionado)

        # 📊 **Cálculos principais**
        total_honorarios_cadastrados = queryset.count()
        total_honorarios = queryset.aggregate(total=Sum("valor_total"))["total"] or 0
        total_pago = queryset.aggregate(pago=Sum("valor_pago"))["pago"] or 0
        total_faltante = total_honorarios - total_pago

        # 📊 **Valores por mês**
        honorarios_por_mes = defaultdict(float)
        pagos_por_mes = defaultdict(float)
        pendentes_por_mes = defaultdict(float)

        for registro in queryset:
            mes = registro.data_vencimento.month
            honorarios_por_mes[mes] += float(registro.valor_total)
            pagos_por_mes[mes] += float(registro.valor_pago)
            pendentes_por_mes[mes] += float(registro.valor_total - registro.valor_pago)

        # Convertendo para JSON para os gráficos
        honorarios_json = json.dumps({int(k): v for k, v in honorarios_por_mes.items()})
        pagos_json = json.dumps({int(k): v for k, v in pagos_por_mes.items()})
        pendentes_json = json.dumps({int(k): v for k, v in pendentes_por_mes.items()})

        # Atualizando o contexto
        context.update({
            "total_honorarios_cadastrados": total_honorarios_cadastrados,
            "total_honorarios": total_honorarios,
            "total_pago": total_pago,
            "total_faltante": total_faltante,
            "anos": [a.year for a in anos],
            "meses": meses,
            "ano_selecionado": ano_selecionado,
            "mes_selecionado": mes_selecionado,
            "honorarios_json": honorarios_json,
            "pagos_json": pagos_json,
            "pendentes_json": pendentes_json,
        })

        return context