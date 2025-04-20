from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_superuser(self, cpf, password=None, **extra_fields):
        
        if not cpf:
            raise ValueError('O CPF deve ser informado')
        usuario = self.model(cpf=cpf, **extra_fields)
        usuario.set_password(password) 
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=20)
    numero_cartao = models.CharField(max_length=16)
    validade_cartao = models.CharField(max_length=5)  
    cvc = models.CharField(max_length=3)

    USERNAME_FIELD = 'cpf' 

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:  
            self.username = self.cpf
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo
    

class Bicicleta(models.Model):
    TIPO_BICICLETA = [
        ('eletrica', 'Elétrica'),
        ('passeio', 'Passeio'),
        ('urbana', 'Urbana'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_BICICLETA)
    status = models.BooleanField(default=True)  
    codigo = models.CharField(max_length=10, unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.codigo}"    

class Aluguel(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_bicicleta = models.CharField(max_length=50)  
    codigo = models.CharField(max_length=6)
    inicio_aluguel = models.DateTimeField(default=now)
    fim_aluguel = models.DateTimeField(null=True, blank=True)
    tempo_total = models.FloatField(null=True, blank=True)
    devolvida = models.BooleanField(default=False)

    def duracao_aluguel(self):
        if self.fim_aluguel:
            return self.fim_aluguel - self.inicio_aluguel
        return None
    
    def __str__(self):
        return f"Aluguel de {self.tipo_bicicleta} por {self.usuario.username}"