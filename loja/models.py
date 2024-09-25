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
        return str(self.nome)

class Categoria(models.Model): # Celular, fone, carregador, capinha, etc
    nome = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str: # Define o método que mostra o nome no /admin/
        return str(self.nome)

class Tipo(models.Model): # Tipo de celular, tipo de fone, tipo de carregador, etc
    nome = models.CharField(max_length=200, null=True, blank=True)

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

class ItemEstoque(models.Model):
    cor = models.CharField(max_length=200, null=True, blank=True)
    tamanho = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Produto

class Endereco(models.Model):
    rua = models.CharField(max_length=400, null=True, blank=True)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)

    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Cliente

class Pedido(models.Model):
    finalizado = models.BooleanField(default=False)
    codigo_transacao = models.CharField(max_length=200, null=True, blank=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Cliente
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para Endereco

class ItensPedido(models.Model):
    quantidade = models.IntegerField(default=0)

    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para ItemEstoque
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)
    # Chave estrangeira para ItemEstoquPedido

class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
       return f"{self.link_destino} - Ativo: {self.ativo}" 