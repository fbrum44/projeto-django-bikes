
from os import name
from django.urls import path
from app_cad_usuarios import views
from django.contrib import admin 

urlpatterns = [
    # rota, view responsável, nome de referência
    # usuarios.com
    path('',views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastroSucesso/', views.cadastroSucesso, name='cadastroSucesso'),
    path('alugarOuDevolver/', views.alugarOuDevolver, name='alugarOuDevolver'),
    path('alterarCadastro/', views.alterarCadastro, name='alterarCadastro'),
    path('alteracaoSucesso/', views.alteracaoSucesso, name='alteracaoSucesso'),
    path('confirmarExclusao/', views.confirmarExclusao, name='confirmarExclusao'),
    path('excluidoSucesso/', views.excluidoSucesso, name='excluidoSucesso'),
    path('alugarBicicleta/', views.alugarBicicleta, name='alugarBicicleta'),
    path('inserirCodigo/', views.inserirCodigo, name='inserirCodigo'),
    path('bicicletaLiberada/', views.bicicletaLiberada, name='bicicletaLiberada'),
    path('devolverBicicleta/', views.devolverBicicleta, name='devolverBicicleta'),
    path('bicicletaDevolvida/<int:aluguel_id>/', views.bicicletaDevolvida, name='bicicletaDevolvida'),
    path('verHistorico/', views.verHistorico, name='verHistorico'),
    path('admin/', admin.site.urls),
]
