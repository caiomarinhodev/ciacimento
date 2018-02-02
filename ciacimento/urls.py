"""urls.py: Urls definidas."""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views.ClientesView import ClientesGerenteListView
from app.views.ClientesView import ClientesVendedorListView
from app.views.HomeView import HomeView
from app.views.LoginView import LoginView, LogoutView, submit_message
from app.views.LojaView import ListProducts, ProductDetail, CarrinhoView, add_item_carrinho, remove_item_carrinho, \
    RegistroClienteView
from app.views.NotificationView import notificar_novo_pedido_vendedor, notificar_novo_pedido_loja, NotificacoesListView
from app.views.PainelGerente import ListPedidosGerente, ListPedidosMesGerente, ListPedidosSemanaGerente, \
    ListPedidosHojeGerente
from app.views.PainelVendedor import ListPedidosVendedor, PedidoUpdateVendedorView, PedidoDetailVendedorView, \
    buscar_cliente
from app.views.PainelVendedor import PedidoCreateVendedorView
from app.views.EntradaView import *
from app.views.SaidaView import *

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
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^admin/login/$', auth_views.login, name='admin_login'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^account/logout/$', LogoutView.as_view(), name='auth_logout'),
    url(r'^submit-contact', submit_message, name='submit_contact'),
    url(r'^catalogo/$', ListProducts.as_view(), name='catalogo'),
    url(r'^registro-login/$', RegistroClienteView.as_view(), name='registro_login'),
    url(r'^produto/(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name='produto'),
    url(r'^add-carrinho/(?P<id_produto>[0-9]+)/$', add_item_carrinho, name='add_carrinho'),
    url(r'^pedido/(?P<pk>[0-9]+)/$', CarrinhoView.as_view(), name='carrinho'),
    url(r'^remove-carrinho/(?P<id_item>[0-9]+)/(?P<id_pedido>[0-9]+)/$', remove_item_carrinho,
        name='delete_carrinho'),

    url(r'^buscar-cliente/$', buscar_cliente, name='buscar-cliente'),

    url(r'^app/pedidos/vendedor/$', ListPedidosVendedor.as_view(), name='pedidos_vendedor'),
    url(r'^app/pedidos/gerente/$', ListPedidosGerente.as_view(), name='pedidos_gerente'),
    url(r'^app/pedidos/vendedor/add/$', PedidoCreateVendedorView.as_view(), name='add_pedido_vendedor'),
    url(r'^app/pedido/(?P<pk>[0-9]+)/edit/$', PedidoUpdateVendedorView.as_view(), name="edit_pedido_vendedor"),
    url(r'^app/pedido/(?P<pk>[0-9]+)/view/$', PedidoDetailVendedorView.as_view(), name="view_pedido_vendedor"),

    url(r'^app/notificacoes/$', NotificacoesListView.as_view(), name='notificacoes'),
    url(r'^notificacao/novo-pedido-vendedor/$', notificar_novo_pedido_vendedor, name="notify_novo_pedido_vendedor"),
    url(r'^notificacao/novo-pedido-loja/$', notificar_novo_pedido_loja, name="notify_novo_pedido_loja"),

    url(r'^app/clientes-gerente/$', ClientesGerenteListView.as_view(), name='list_clientes_gerente'),
    url(r'^app/clientes-vendedor/$', ClientesVendedorListView.as_view(), name='list_clientes_vendedor'),

    url(r'^app/entradas/$', EntradaListView.as_view(), name='list_entradas'),
    url(r'^app/entradas/add/$', EntradaCreateView.as_view(), name='add_entrada'),
    url(r'^app/entradas/(?P<pk>[0-9]+)/$', EntradaDetailView.as_view(), name='view_entrada'),
    url(r'^app/entradas/(?P<pk>[0-9]+)/edit$', EntradaEditView.as_view(), name='edit_entrada'),

    url(r'^app/saidas/$', SaidaListView.as_view(), name='list_saidas'),
    url(r'^app/saidas/add/$', SaidaCreateView.as_view(), name='add_saida'),
    url(r'^app/saidas/(?P<pk>[0-9]+)/$', SaidaDetailView.as_view(), name='view_saida'),
    url(r'^app/saidas/(?P<pk>[0-9]+)/edit$', SaidaEditView.as_view(), name='edit_saida'),

    url(r'^app/pedidos/mes/gerente/$', ListPedidosMesGerente.as_view(), name='pedidos_mes_g'),
    url(r'^app/pedidos/semana/gerente/$', ListPedidosSemanaGerente.as_view(), name='pedidos_semana_g'),
    url(r'^app/pedidos/hoje/gerente/$', ListPedidosHojeGerente.as_view(), name='pedidos_hoje_g'),

]
