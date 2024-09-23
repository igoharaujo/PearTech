from django.shortcuts import render
from .models import *

# A cada nova pag HTML em /templates uma função com o nome da página 
# deve ser criada, seguindo o padrão das demais funções. A função deve
# ser passada no arquivo urls.py para funcionar.

def homepage(request):
    return render(request, 'homepage.html')

def loja(request):
    produtos = Produto.objects.all()
    context = { "produtos" : produtos }
    return render(request, 'loja.html', context)

def carrinho(request):
    return render(request, 'carrinho.html')

def checkout(request):
    return render(request, 'checkout.html')

# Relacionados a login e conta do usuario
def minhaconta(request):
    return render(request, 'usuario/minhaconta.html')

def login(request):
    return render(request, 'usuario/login.html')