from .models import CustomUser, Aluguel
from .forms import CadastroForm, AlterarCadastroForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

def cadastrar_usuario(data):
    form = CadastroForm(data)
    if form.is_valid():
        usuario = form.save()
        return usuario, None
    return None, form.errors   

def autenticar_usuario(request, cpf, password):
    usuario = authenticate(request, cpf=cpf, password=password)
    if usuario:
        login(request, usuario)
        return usuario
    return None 

def alterar_usuario(user, data):
      form = AlterarCadastroForm(data, instance=user)
      if form.is_valid():
            for field, value in form.cleaned_data.items():
                if value:  
                    setattr(user, field, value)
            
            senha = form.cleaned_data.get('password1')
            if senha:
                user.password = make_password(senha)
            user.save()
            return True, None
      return False, form.errors

def criar_aluguel(usuario_id, tipo_bicicleta, codigo_desbloqueio=None):
    if not tipo_bicicleta:
        return None, "Erro: Nenhuma bicicleta selecionada."
    
    if not codigo_desbloqueio:
        return None, "Erro: Código de desbloqueio inválido."
    
    aluguel = Aluguel.objects.create(
        usuario_id=usuario_id,
        tipo_bicicleta=tipo_bicicleta,
        codigo=codigo_desbloqueio,
        inicio_aluguel=now(),
        devolvida=False
    )
    return aluguel, None
