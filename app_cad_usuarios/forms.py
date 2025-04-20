from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class CadastroForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['nome_completo', 'email', 'telefone', 'cpf', 'rg', 'numero_cartao', 'validade_cartao', 'cvc']
       
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("password1")
        confirmar_senha = cleaned_data.get("password2")

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('password2', "As senhas não correspondem.")

        if senha and not senha.isdigit():  
            self.add_error('password1', "A senha deve conter apenas números.")    

        return cleaned_data

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if cpf:
            cpf = cpf.replace(".", "").replace("-", "")
            
            if not cpf.isdigit() or len(cpf) != 11:
                raise forms.ValidationError("Digite um CPF válido com 11 números.")
        
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  
        if commit:
            user.save()
        return user  
    
class AlterarCadastroForm(UserCreationForm):
    password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite uma nova senha'}),
        required=False  
    )
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a nova senha'}),
        required=False  
    )
    class Meta:
        model = CustomUser
        fields = ['nome_completo', 'email', 'telefone', 'numero_cartao', 'validade_cartao', 'cvc']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("password1")
        confirmar_senha = cleaned_data.get("password2")

        if senha or confirmar_senha:
            if senha != confirmar_senha:
                self.add_error('password2', "As senhas não correspondem.")
            elif not senha.isdigit():
                self.add_error('password1', "A senha deve conter apenas números.")

        return {key: value for key, value in cleaned_data.items() if value}

class EscolherBicicletaForm(forms.Form):
    
    TIPO_BICICLETA = [
        ('eletrica', 'Elétrica'),
        ('passeio', 'Passeio'),
        ('urbana', 'Urbana'),
    ]

    bicicleta = forms.ChoiceField(
        choices=TIPO_BICICLETA,
        widget=forms.RadioSelect(attrs={'class': 'bicicleta-radio'}),
        label="Escolha o tipo de bicicleta"
    )    

    
