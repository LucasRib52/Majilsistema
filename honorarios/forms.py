from django import forms
from .models import Honorario
from clientes.models import Cliente

class HonorarioForm(forms.ModelForm):
    cliente_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )

    cliente_nome = forms.CharField(
        label="Cliente",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do cliente...', 'autocomplete': 'off'}),
        required=False  # Esse campo é só para exibição
    )

    class Meta:
        model = Honorario
        fields = ['valor_total']  # 🔥 Removemos 'data_vencimento'


    def clean_cliente_id(self):
        cliente_id = self.cleaned_data.get('cliente_id')

        if not cliente_id:
            raise forms.ValidationError("Cliente não encontrado. Selecione um cliente válido.")

        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            raise forms.ValidationError("Cliente não encontrado. Selecione um cliente válido.")

        # 🔥 IMPEDINDO DUPLICAÇÃO DE HONORÁRIOS
        if Honorario.objects.filter(cliente=cliente).exists():
            raise forms.ValidationError("Já existe um honorário cadastrado para esta empresa!")

        return cliente

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.cliente = self.cleaned_data['cliente_id']  # Define o cliente corretamente

        if commit:
            instance.save()
        return instance

# **📌 Novo formulário para pagamento com comprovante**
class PagamentoForm(forms.ModelForm):
    valor_pago = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Valor Pago",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    comprovante = forms.FileField(
        label="Comprovante de Pagamento (opcional)",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Honorario
        fields = ['valor_pago', 'comprovante']

    def __init__(self, *args, **kwargs):
        self.honorario = kwargs.pop('honorario', None)
        super().__init__(*args, **kwargs)

    def clean_valor_pago(self):
        valor_pago = self.cleaned_data.get('valor_pago')

        if valor_pago is None or valor_pago <= 0:
            raise forms.ValidationError("O valor do pagamento deve ser positivo e com até duas casas decimais.")
        
        if self.honorario:
            valor_restante = self.honorario.valor_total - self.honorario.valor_pago
            if valor_pago > valor_restante:
                raise forms.ValidationError(f"O valor não pode exceder o restante de R$ {valor_restante:.2f}.")

        return valor_pago


class HonorarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Honorario
        fields = ['valor_total', 'observacao']  # Adicionando o campo observacao

    valor_total = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Valor do Honorário (R$)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    )

    observacao = forms.CharField(
        required=False,
        label="Observação",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )

    def save(self, commit=True):
        # ✅ Agora, apenas o objeto atual é salvo, sem alterar todos os registros do cliente
        return super().save(commit)

