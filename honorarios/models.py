import os
import datetime
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from clientes.models import Cliente

class Honorario(models.Model):
    STATUS_PAGAMENTO = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total do Honorário")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Pago")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento", null=False, blank=False)
    status_pagamento = models.CharField(max_length=10, choices=STATUS_PAGAMENTO, default='pendente', verbose_name="Status do Pagamento")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    comprovante = models.FileField(upload_to="comprovantes/Honorario", null=True, blank=True, verbose_name="Comprovante de Pagamento")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    def save(self, *args, **kwargs):
        # ✅ Define a data de vencimento automática se não estiver definida
        if not self.data_vencimento:
            hoje = datetime.date.today()
            self.data_vencimento = datetime.date(hoje.year, hoje.month, 10)

        # ✅ Se o valor pago for igual ou maior que o total, marca como pago
        if self.valor_pago >= self.valor_total:
            self.status_pagamento = 'pago'
        else:
            self.status_pagamento = 'pendente'

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # ✅ Exclui o comprovante ao deletar o honorário
        if self.comprovante and os.path.isfile(self.comprovante.path):
            os.remove(self.comprovante.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente.nome_empresa} - R$ {self.valor_total} ({self.get_status_pagamento_display()})"

    class Meta:
        verbose_name = "Honorário"
        verbose_name_plural = "Honorários"
        ordering = ['-data_vencimento']


# 🔹 Criar automaticamente os próximos meses e o próximo ano ao cadastrar um novo honorário
@receiver(post_save, sender=Honorario)
def criar_proximos_honorarios(sender, instance, created, **kwargs):
    if created:  # ✅ Somente ao criar um novo honorário
        hoje = datetime.date.today()
        ano_atual = hoje.year

        # ✅ Criar honorários até o final de 2025 e também 2026
        for ano in [ano_atual, ano_atual + 1]:  # 🔥 Agora gera para o ano atual e o próximo (2026)
            for mes in range(1, 13):  # 🔥 Gera todos os meses de janeiro a dezembro
                data_vencimento = datetime.date(ano, mes, 10)

                # ✅ Evita criar honorários duplicados
                if not Honorario.objects.filter(cliente=instance.cliente, data_vencimento=data_vencimento).exists():
                    Honorario.objects.create(
                        cliente=instance.cliente,
                        valor_total=instance.valor_total,
                        valor_pago=0.00,  # Sempre inicia como pendente
                        data_vencimento=data_vencimento,
                        status_pagamento='pendente'
                    )


# 🔹 Excluir todos os honorários futuros do mesmo cliente ao excluir um honorário
@receiver(pre_delete, sender=Honorario)
def excluir_honorarios_futuros(sender, instance, **kwargs):
    """ Remove todos os honorários do mesmo cliente que são futuros e ainda estão pendentes """
    Honorario.objects.filter(
        cliente=instance.cliente,
        data_vencimento__gt=instance.data_vencimento,  # Apenas os futuros
        status_pagamento='pendente'  # Mantém os que já foram pagos
    ).delete()
