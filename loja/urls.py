from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name="homepage"), # link, função e nome da página
    path('loja/', loja, name="loja"),
    path('loja/<str:filtro>/', loja, name="loja"),
    path('produto/<int:id_produto>/', ver_produto, name='ver_produto'),
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name='ver_produto'),
    path('minhaconta/', minhaconta, name="minha_conta"),
    path('login/', login, name="login"),
    path('carrinho/', carrinho, name="carrinho"), 
    path('adicionar-carrinho/<int:id_produto>/', adicionar_carrinho, name="adicionar_carrinho"),
    path('remover-carrinho/<int:id_produto>/', remover_carrinho, name="remover_carrinho"),
    path('checkout/', checkout, name='checkout'),
    path('adicionar-endereco/', adicionar_endereco, name='adicionar_endereco'),
]

# path('loja/<str:nome_categoria>/', loja, name="loja")

# Sempre que houver um parâmetro como '<str:nome_categoria>', ele 
# deve ser adicionado na chamada da função correspondente ao url