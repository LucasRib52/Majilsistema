from django.db import models

class Condominio(models.Model):
    TIPO_UNIDADE = [
        ('sala', 'Sala'),
        ('loja', 'Loja'),
    ]

    nome = models.CharField(max_length=255)
    tipo_unidade = models.CharField(max_length=5, choices=TIPO_UNIDADE)
    numero_sala = models.CharField(max_length=10, blank=True, null=True)
    numero_loja = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nome


class PagamentoCondominio(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    comprovante = models.FileField(blank=True, null=True, upload_to='comprovantes/Condominio')
    data_pagamento = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, default='pago')  # Sempre será "pago"

    def __str__(self):
        return f"Pagamento de {self.valor} - {self.condominio.nome} (Pago)"
