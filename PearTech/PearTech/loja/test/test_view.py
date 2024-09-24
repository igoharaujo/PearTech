import pytest
from django.test import RequestFactory
from loja.views import homepage
from loja.models import Banner

@pytest.mark.django_db
def test_homepage_view():
    factory = RequestFactory()
    request = factory.get('/')
    
    # Cria alguns banners de teste
    Banner.objects.create(imagem="banner1.jpg", link_destino="http://example.com/1", ativo=True)
    Banner.objects.create(imagem="banner2.jpg", link_destino="http://example.com/2", ativo=False)
    Banner.objects.create(imagem="banner3.jpg", link_destino="http://example.com/3", ativo=True)
    
    response = homepage(request)
    
    assert response.status_code == 200

