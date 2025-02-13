import datetime
from django.core.management.base import BaseCommand
from honorarios.models import Honorario

class Command(BaseCommand):
    help = 'Atualiza os honorários para o novo mês, mantendo-os fixos e colocando como pendente se necessário.'

    def handle(self, *args, **kwargs):
        hoje = datetime.date.today()
        primeiro_dia_mes = hoje.replace(day=1)

        # Verifica se já existem honorários gerados para este mês
        if Honorario.objects.filter(data_vencimento__year=hoje.year, data_vencimento__month=hoje.month).exists():
            self.stdout.write(self.style.WARNING("Os honorários deste mês já foram gerados. Nenhuma ação necessária."))
            return

        # Pega todos os honorários do mês anterior
        honorarios_anterior = Honorario.objects.filter(
            data_vencimento__year=primeiro_dia_mes.year,
            data_vencimento__month=primeiro_dia_mes.month - 1
        )

        if not honorarios_anterior.exists():
            self.stdout.write(self.style.WARNING("Nenhum honorário encontrado no mês anterior para replicação."))
            return

        # Criar novos honorários para o mês atual
        novos_honorarios = []
        for honorario in honorarios_anterior:
            novo_honorario = Honorario(
                cliente=honorario.cliente,
                valor_total=honorario.valor_total,
                valor_pago=0.00,  # Sempre inicia o novo mês como pendente
                data_vencimento=hoje.replace(day=10),
                status_pagamento='pendente'
            )
            novos_honorarios.append(novo_honorario)

        Honorario.objects.bulk_create(novos_honorarios)
        self.stdout.write(self.style.SUCCESS("Honorários atualizados para o novo mês com sucesso!"))
