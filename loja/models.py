from django.db import models
from django.contrib.auth.models import User

#Criação de Tabelas:

class Cliente(models.Model): 
    nome = models.CharField(max_length=200, null=True, blank=True) 
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    id_sessao = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) 
    # Relacionamento 1 -> 1 para a tabela User nativa do django.
    # DELETE CASCADE!!! CUIDADO!!!

    def __str__(self) -> str: # Define o método que mostra o nome no /admin/
        if self.email:
            return str(self.email)
        else:
            return f"cliente anônimo"

class Categoria(models.Model): # Celular, fone, carregador, capinha, etc
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str: # Define o método que mostra o nome no /admin/
        return str(self.nome)

class Tipo(models.Model): # Tipo de celular, tipo de fone, tipo de carregador, etc
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Categoria

    def __str__(self) -> str: # Define o método que mostra o nome no /admin/
        return str(self.nome)

class Produto(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Categoria
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Tipo

    def __str__(self) -> str: # Define o método que mostra o nome no /admin/
        return f"Nome: {self.nome}, Categoria: {self.categoria}, Tipo: {self.tipo}, Preço: {self.preco}"
    
    def total_vendas(self):
        itens = ItensPedido.objects.filter(pedido__finalizado=True, item_estoque__produto=self.id)
        total =  sum([item.quantidade for item in itens])
        return total

class Cor(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.nome)
class ItemEstoque(models.Model):
    modelo = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    cor = models.ForeignKey(Cor, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Cor

    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Produto
    
    def __str__(self) -> str: # Define o método que mostra o nome no /admin/
        return f"{self.produto.nome} - Cor: {self.cor.nome} - Modelo: {self.modelo}"

class Endereco(models.Model):
    rua = models.CharField(max_length=400, null=True, blank=True)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)

    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Cliente

    def __str__(self) -> str:
        return f"Endereço [{self.id}] de: {str(self.cliente)} - {self.cep}"

class Pedido(models.Model):
    finalizado = models.BooleanField(default=False)
    codigo_transacao = models.CharField(max_length=200, null=True, blank=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Cliente
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Endereco

    def __str__(self) -> str:
        return str(f"id_pedido [ {self.id} ] - {self.cliente} - finalizado [ {self.finalizado} ] ")
    
    @property
    def quantidade_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido_id=self.id)
        quantidade = sum(
            [item.quantidade for item in itens_pedido]
        )
        return quantidade
 
    @property
    def preco_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido_id=self.id)
        preco = sum(
            [item.preco_total for item in itens_pedido]
        )
        return preco
    
    @property
    def itens(self):
        itens_pedido = ItensPedido.objects.filter(pedido_id=self.id)
        return itens_pedido
class ItensPedido(models.Model):
    quantidade = models.IntegerField(default=0)

    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para ItemEstoque
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Pedido

    def __str__(self) -> str:
        itempedido = str(f"id_pedido [ {self.id} ] - produto [ {self.item_estoque.produto.nome}, {self.item_estoque.cor}, {self.item_estoque.modelo} ]")
        return itempedido
    
    @property
    def preco_total(self):
        return self.quantidade * self.item_estoque.produto.preco

class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self) -> str:
       return f"{self.link_destino} - Ativo: {self.ativo}" 

class Pagamento(models.Model):
    id_pagamento = models.CharField(max_length=400)
    aprovado = models.BooleanField(default=False)

    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Pedido