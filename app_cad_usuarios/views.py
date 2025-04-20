from unittest import installHandler
from django.shortcuts import render, redirect
from .forms import CadastroForm
from .controller import cadastrar_usuario, autenticar_usuario, alterar_usuario, criar_aluguel
from django.contrib.auth import logout
from django.contrib import messages
from app_cad_usuarios.models import CustomUser
from app_cad_usuarios.forms import AlterarCadastroForm
import time
import datetime
import random
from django.http import HttpResponse
from django.utils.timezone import now
from .models import Aluguel
from django.db.models import Sum

def home(request):
    return render(request, 'usuarios/home.html')

def cadastro(request): 
    if request.method == "POST":
        usuario, erros = cadastrar_usuario(request.POST)
        if usuario:
            return redirect('cadastroSucesso')
        else:
            print(erros)
            return render(request, 'usuarios/cadastro.html', {'form': request.POST, 'errors': erros})
    else:
        form = CadastroForm(data=request.POST)    
    return render(request, 'usuarios/cadastro.html')

def cadastroSucesso(request):
    return render(request, 'usuarios/cadastroSucesso.html')

def login_view(request):
    if request.method =='POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('senha')

        usuario = autenticar_usuario(request, cpf=cpf, password=password)

        if usuario is not None:
            next_page = request.GET.get('next', 'alugarOuDevolver')
            return redirect(next_page)
    
        else:  
            messages.error(request, "CPF ou senha incorretos")
            return redirect('home')
    else:
        return render(request, 'usuarios/home.html')    


def alugarOuDevolver(request):  
    user_id = request.session.get('_auth_user_id')
    
    if user_id:
        user = CustomUser.objects.get(id=user_id)  
        return render(request, 'usuarios/alugarOuDevolver.html', {'user': user})

    else:
        return render(request, 'erro.html', {'mensagem': 'Usuário não autenticado'})
   

def logout_view(request):
    logout(request)
    return redirect('home')

def alterarCadastro(request):
    user_id = request.session.get('_auth_user_id')

    if not user_id:
        return render(request, 'erro.html', {'mensagem': 'Usuário não autenticado'})
     
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return render(request, 'erro.html', {'mensagem': 'Usuário não encontrado'})
    
    if request.method == 'POST':
        sucesso, erros = alterar_usuario(user, request.POST)
        if sucesso:
            return redirect('alteracaoSucesso')
        else:
            form = AlterarCadastroForm(request.POST, instance=user)
            return render(request, 'usuarios/alterarCadastro.html', {'form': request.POST, 'errors': erros})
    else:
        form = AlterarCadastroForm(instance=user)

    return render(request, 'usuarios/alterarCadastro.html', {'form': form})

def alteracaoSucesso(request):
    return render(request, 'usuarios/alteracaoSucesso.html')

def confirmarExclusao(request):
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return render(request, 'erro.html', {'mensagem': 'Usuário não autenticado'})
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return render(request, 'erro.html', {'mensagem': 'Usuário não encontrado'})
    
    if request.method == 'POST':
        user.delete()
        logout(request)  
        return redirect('excluidoSucesso')
    
    return render(request, 'usuarios/confirmarExclusao.html', {'user': user})

def excluidoSucesso(request):
    return render(request, 'usuarios/excluidoSucesso.html')

def alugarBicicleta(request):
    
    user_id = request.session.get('_auth_user_id')
    
    if not user_id:
        return HttpResponse("Erro: Usuário não autenticado", status=403)
    
    if request.method == "POST":
        tipo_bicicleta = request.POST.get('bicicleta')

        if not tipo_bicicleta:
            return HttpResponse("Erro: Nenhuma bicicleta selecionada", status=400)
        
        request.session['bicicleta'] = tipo_bicicleta

        return redirect('inserirCodigo')

    return render(request, 'usuarios/alugarBicicleta.html')

def inserirCodigo(request):
    
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return HttpResponse("Erro: Usuário não autenticado", status=403)

    if 'codigo_desbloqueio' not in request.session:
        codigo_desbloqueio = random.randint(1000, 9999)
        request.session['codigo_desbloqueio'] = codigo_desbloqueio

    if request.method == "POST":
        codigo = request.POST.get('codigo')
        
        if codigo and int(codigo) == request.session['codigo_desbloqueio']:
            tipo_bicicleta = request.session.get('bicicleta')
        
            if tipo_bicicleta:
                aluguel, erro = criar_aluguel(user_id, tipo_bicicleta, request.session['codigo_desbloqueio'])

           
            if erro:
                return render(request, 'erro.html', {'mensagem': erro})
            
            request.session['codigo_aluguel'] = aluguel.id
            request.session['tempo_inicio'] = time.time()

            return redirect('bicicletaLiberada') 
        else:
            return render(request, 'usuarios/inserirCodigo.html', {
                'codigo_desbloqueio': request.session['codigo_desbloqueio'],
                'error_message': "Código inválido. Tente novamente."
            })

    return render(request, 'usuarios/inserirCodigo.html', {'codigo_desbloqueio': request.session['codigo_desbloqueio']})

def bicicletaLiberada(request):
    
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return HttpResponse("Erro: Usuário não autenticado", status=403)
    
    codigo_aluguel = request.session.get('codigo_aluguel')
    tempo_inicio = request.session.get('tempo_inicio')

    if not codigo_aluguel or not tempo_inicio:
        return HttpResponse("Erro: Código não validado ou tempo de início não encontrado", status=403)

    return render(request, 'usuarios/bicicletaLiberada.html', {'tempo_inicio': tempo_inicio})

def devolverBicicleta(request):
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return HttpResponse("Erro: Usuário não autenticado", status=403)
    
    
    aluguel = Aluguel.objects.filter(usuario_id=user_id, fim_aluguel__isnull=True).first()
    if not aluguel:
        return HttpResponse("Erro: Nenhuma bicicleta ativa encontrada para devolução.", status=404)

    if 'codigo_devolucao' not in request.session:
        codigo_devolucao = random.randint(1000, 9999)
        request.session['codigo_devolucao'] = codigo_devolucao

    if request.method == "POST":
        codigo = request.POST.get('codigo')

        if codigo and int(codigo) == request.session['codigo_devolucao']:
            aluguel.fim_aluguel = now()
            aluguel.save()

            del request.session['codigo_devolucao']

            return redirect('bicicletaDevolvida', aluguel_id=aluguel.id)

        else:
            return render(request, 'usuarios/devolverBicicleta.html', {
                'codigo_devolucao': request.session['codigo_devolucao'],
                'error_message': "Código inválido. Tente novamente.",
                'tipo_bicicleta': aluguel.tipo_bicicleta
            })

    return render(request, 'usuarios/devolverBicicleta.html', {
        'codigo_devolucao': request.session['codigo_devolucao'],
        'tipo_bicicleta': aluguel.tipo_bicicleta
    })

def bicicletaDevolvida(request, aluguel_id):
   
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return HttpResponse("Erro: Usuário não autenticado", status=403)
    
    aluguel = Aluguel.objects.filter(id=aluguel_id, usuario_id=user_id, fim_aluguel__isnull=False).first()
    if not aluguel:
        return HttpResponse("Erro: Não foi possível encontrar o aluguel ou a bicicleta não foi devolvida.", status=404)

    tempo_inicio_sessao = request.session.get('tempo_inicio')
    if not tempo_inicio_sessao:
        return HttpResponse("Erro: Tempo de início não encontrado.", status=404)
    
    tempo_inicio = datetime.datetime.fromtimestamp(tempo_inicio_sessao)
    
    tempo_fim = datetime.datetime.now()  
    tempo_total = tempo_fim - tempo_inicio
    tempo_total_segundos = tempo_total.total_seconds()

        
    minutos_usados = tempo_total_segundos // 60
    segundos_usados = tempo_total_segundos % 60

    tempo_usado = f"{int(minutos_usados)} minutos e {int(segundos_usados)} segundos"

    aluguel.tempo_total = tempo_total_segundos
    aluguel.save()
    

    return render(request, 'usuarios/bicicletaDevolvida.html', {
        'tempo_usado': tempo_usado,
        'aluguel': aluguel
    })

def verHistorico(request):
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return HttpResponse("Erro: Usuário não autenticado", status=403)
    
    alugueis = Aluguel.objects.filter(usuario_id=user_id, tempo_total__isnull=False)

    tempos_por_bicicleta = alugueis.values('tipo_bicicleta').annotate(total_tempo=Sum('tempo_total'))

    historico = []
    for item in tempos_por_bicicleta:
        minutos = int(item['total_tempo'] // 60)
        segundos = int(item['total_tempo'] % 60)
        historico.append({
            'tipo_bicicleta': item['tipo_bicicleta'],
            'tempo': f"{minutos} minutos e {segundos} segundos"
        })

    return render(request, 'usuarios/verHistorico.html', {'historico': historico})
