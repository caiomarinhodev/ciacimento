"""urls.py: Urls definidas."""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views.HomeView import HomeView
# from app.views.LoginView import LoginView, LogoutView, RegisterView, EditarPerfilView, RegisterMotoristaView
from app.views.LoginView import LoginView, LogoutView, submit_message
from app.views.LojaView import ListProducts, ProductDetail, CarrinhoView, add_item_carrinho, remove_item_carrinho, \
    ProcessPedidoView

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"

"""default URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^account/logout/$', LogoutView.as_view(), name='auth_logout'),
    url(r'^submit-contact', submit_message, name='submit_contact'),
    url(r'^catalogo/$', ListProducts.as_view(), name='catalogo'),
    url(r'^produto/(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name='produto'),
    url(r'^add-carrinho/(?P<id_produto>[0-9]+)/$', add_item_carrinho, name='add_carrinho'),
    url(r'^pedido/(?P<pk>[0-9]+)/$', CarrinhoView.as_view(), name='carrinho'),
    url(r'^remove-carrinho/(?P<id_item>[0-9]+)/(?P<id_pedido>[0-9]+)/$', remove_item_carrinho,
        name='delete_carrinho'),

    url(r'^checkout/(?P<pk>[0-9]+)/$', ProcessPedidoView.as_view(), name='checkout'),

]
