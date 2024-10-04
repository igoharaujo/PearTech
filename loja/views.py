from django.shortcuts import render, redirect
from .models import *

# A cada nova pag HTML em /templates uma função com o nome da página 
# deve ser criada, seguindo o padrão das demais funções. A função deve
# ser passada no arquivo urls.py para funcionar.

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners" : banners}
    return render(request, 'homepage.html', context)
    
def loja(request, nome_categoria=None):
    produtos = Produto.objects.filter(ativo=True)
    if nome_categoria:
        produtos = produtos.filter(categoria__nome = nome_categoria)
    context = { "produtos" : produtos }
    return render(request, 'loja.html', context)

def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = {}
    modelos = {}
    cor_selecionada = None
    if id_cor:
        cor_selecionada = Cor.objects.get(id=id_cor)
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = [item.cor for item in itens_estoque] # Armazena as cores de cada item no estoque
        if id_cor:
            itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id=id_cor)
            modelos = {item.modelo for item in itens_estoque} # Fazer isso para MODELOS
    context = {
                "produto": produto,  
                "tem_estoque": tem_estoque, 
                "cores": cores,
                "modelos": modelos,
                "cor_selecionada": cor_selecionada
               }
    return render(request, "ver_produto.html", context)

def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = {"itens_pedido":itens_pedido,
               "pedido":pedido}
    return render(request, 'carrinho.html', context)

def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        print(dados)
        modelo = dados.get("modelo") # Caso o valor nao seja encontrado, retornara None
        id_cor = dados.get("cor")
        if not modelo:
            return redirect('loja')
        return redirect('carrinho')
    else:
        return redirect('loja')

def checkout(request):
    return render(request, 'checkout.html')

# Funções relacionadas a login e conta do usuario
def minhaconta(request):
    return render(request, 'usuario/minhaconta.html')

def login(request):
    return render(request, 'usuario/login.html')

# TODO Sempre que um USER criar uma conta, um cliente será criado para ele