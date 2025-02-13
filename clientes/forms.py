from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_empresa', 'tipo_pessoa', 'cnpj', 'cpf']
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_pessoa = cleaned_data.get("tipo_pessoa")
        cnpj = cleaned_data.get("cnpj")
        cpf = cleaned_data.get("cpf")

        if tipo_pessoa == "CNPJ":
            if not cnpj:
                self.add_error("cnpj", "CNPJ é obrigatório para empresas.")
            cleaned_data["cpf"] = None  # Garante que CPF fique vazio

        elif tipo_pessoa == "CPF":
            if not cpf:
                self.add_error("cpf", "CPF é obrigatório para pessoa física.")
            cleaned_data["cnpj"] = None  # Garante que CNPJ fique vazio

        return cleaned_data
