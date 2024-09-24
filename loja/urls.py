from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name="homepage"), # link, função e nome da página
    path('loja/', loja, name="loja"),
    path('minhaconta/', minhaconta, name="minha_conta"),
    path('login/', login, name="login"),
    path('carrinho/', carrinho, name="carrinho"),
    path('checkout/', checkout, name='checkout'),
]
