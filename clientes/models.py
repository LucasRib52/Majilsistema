from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('CNPJ', 'CNPJ'),
        ('CPF', 'CPF'),
    ]

    nome_empresa = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    tipo_pessoa = models.CharField(max_length=4, choices=TIPO_CHOICES, verbose_name="Tipo de Pessoa")
    
    cnpj = models.CharField(
        max_length=18, 
        blank=True, 
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', 
                message="CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX."
            )
        ],
        verbose_name="CNPJ"
    )

    cpf = models.CharField(
        max_length=14, 
        blank=True, 
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 
                message="CPF deve estar no formato XXX.XXX.XXX-XX."
            )
        ],
        verbose_name="CPF"
    )

    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    def __str__(self):
        return f"{self.nome_empresa} ({self.tipo_pessoa})"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
