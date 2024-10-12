from django.shortcuts import render, redirect
from .models import *
import uuid
from .utils import *


# A cada nova pag HTML em /templates uma função com o nome da página 
# deve ser criada, seguindo o padrão das demais funções. A função deve
# ser passada no arquivo urls.py para funcionar.

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners" : banners}
    return render(request, 'homepage.html', context)
    
def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrar_produtos(produtos, filtro)
    if request.method == "POST":
        dados = request.POST.dict()
        produtos = produtos.filter(preco__gte=dados.get("preco_minimo"), preco__lte=dados.get("preco_maximo"))
        if "modelo" in dados:
            itens = ItemEstoque.objects.filter(produto__in=produtos, modelo=dados.get("modelo"))
            ids_produtos = itens.values_list("produto", flat=True).distinct()
            produtos = Produto.objects.filter(id__in=ids_produtos)
        if "tipo" in dados:
            produtos = produtos.filter(tipo__slug=dados.get("tipo"))
        if "categoria" in dados:
            produtos = produtos.filter(categoria__slug=dados.get("categoria"))
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    modelos = itens.values_list("modelo", flat=True).distinct()
    ids_categorias = produtos.values_list("categoria", flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=ids_categorias)
    minimo, maximo = preco_min_max(produtos)
    context = { 
                "produtos" : produtos,
                "minimo": minimo,
                "maximo": maximo,
                "modelos": modelos,
                "categorias": categorias,
                }
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
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {
                    "cliente_existente":False,
                    "itens_pedido": None,
                    "pedido": None,
                       }
            return render(request, 'carrinho.html', context)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = {
            "itens_pedido":itens_pedido,
            "pedido":pedido,
            "cliente_existente": True,
            }
    return render(request, 'carrinho.html', context)

def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        modelo = dados.get("modelo") # Caso o valor nao seja encontrado, retornara None
        id_cor = dados.get("cor")
        if not modelo:
            return redirect('loja')
        resposta = redirect('carrinho')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
            else:
                id_sessao = str(uuid.uuid4())                         # segundos X minutos X horas X dias 
                resposta.set_cookie(key="id_sessao", value=id_sessao, max_age=60*60*24*30) 
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, modelo=modelo, cor__id=id_cor)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save() #Salvar toda vez que editar um elemento do banco de dados
        return resposta
    else:
        return redirect('loja')

def remover_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        modelo = dados.get("modelo") # Caso o valor nao seja encontrado, retornara None
        id_cor = dados.get("cor")
        if not modelo:
            return redirect('loja')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, modelo=modelo, cor__id=id_cor)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade -= 1
        item_pedido.save() #Salvar toda vez que editar um elemento do banco de dados
        if item_pedido.quantidade <= 0:
            item_pedido.delete()
        return redirect('carrinho')
    else:
        return redirect('loja')

def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect('loja')
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {
            "pedido":pedido,
            "enderecos":enderecos,
            }
    return render(request, 'checkout.html', context)

def adicionar_endereco(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        dados = request.POST.dict()
        endereco = Endereco.objects.create(cliente=cliente, 
                                           rua=dados.get("rua"),
                                           numero=int(dados.get("numero")),
                                           estado=dados.get("estado"),
                                           cidade=dados.get("cidade"),
                                           cep=dados.get("cep"),
                                           complemento=dados.get("complemento"),
                                           )
        endereco.save()
        return redirect('checkout')
    else:
        context = {}
        return render(request, 'adicionar_endereco.html', context)

# Funções relacionadas a login e conta do usuario
def minhaconta(request):
    return render(request, 'usuario/minhaconta.html')

def login(request):
    return render(request, 'usuario/login.html')

# TODO Sempre que um USER criar uma conta, um cliente será criado para ele