from django import forms
from .models import Condominio, PagamentoCondominio

class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'tipo_unidade', 'numero_sala', 'numero_loja']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicando classes Bootstrap aos campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Placeholders personalizados
        self.fields['nome'].widget.attrs['placeholder'] = 'Digite o nome do condomínio'
        self.fields['numero_sala'].widget.attrs['placeholder'] = 'Digite o número da sala'
        self.fields['numero_loja'].widget.attrs['placeholder'] = 'Digite o número da loja'

        # Escondendo os campos até que a opção correta seja selecionada
        self.fields['numero_sala'].widget.attrs['style'] = 'display: none;'
        self.fields['numero_loja'].widget.attrs['style'] = 'display: none;'


class PagamentoCondominioForm(forms.ModelForm):
    class Meta:
        model = PagamentoCondominio
        fields = ['condominio', 'valor', 'descricao', 'comprovante']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicando classes Bootstrap aos campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Placeholders personalizados
        self.fields['valor'].widget.attrs['placeholder'] = 'Digite o valor do pagamento'
        self.fields['descricao'].widget.attrs['placeholder'] = 'Adicione uma descrição opcional'
