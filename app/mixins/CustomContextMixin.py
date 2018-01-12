# coding=utf-8
from datetime import datetime

from django.views.generic.base import ContextMixin
from django.contrib import messages
from django.views.generic import ListView
from app.models import *
from django.shortcuts import redirect
from django.contrib.auth import logout


class RedirectMotoristaOcupadoView(ListView):
    def get(self, request, *args, **kwargs):
        motorista = None
        try:
            motorista = Motorista.objects.get(user=self.request.user)
        except:
            pass
        if motorista:
            if motorista.ocupado:
                return redirect('route_pedido_view', **{'pk': motorista.user.pedido_set.last().pk})
        return super(RedirectMotoristaOcupadoView, self).get(request, *args, **kwargs)


class CustomContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        if 'pedido' in self.request.session:
            kwargs['pedido'] = Pedido.objects.get(id=self.request.session['pedido'])
        return super(CustomContextMixin, self).get_context_data(**kwargs)

# class DashboardMixin(ContextMixin):
#     def get_context_data(self, **kwargs):
#         now = datetime.now()
#         motoristas = Motorista.objects.all()
#         pedidos = Pedido.objects.all()
#         users = User.objects.all()
#         notificacoes = Notification.objects.all()
#         locations = Location.objects.all()
#         bairros = Bairro.objects.all()
#         estabelecimentos = Estabelecimento.objects.all()
#         pontos = Ponto.objects.all()
#         kwargs['motoristas'] = motoristas
#         kwargs['pedidos'] = pedidos
#         kwargs['users'] = users
#         kwargs['estabelecimentos'] = estabelecimentos
#         kwargs['bd_space'] = float(float(float(
#             len(motoristas) + len(pedidos) + len(users) + len(notificacoes) + len(locations) + len(bairros) + len(
#                 estabelecimentos) + len(pontos)) / 10000) * 100)
#         kwargs['num_pedidos_entregues'] = Pedido.objects.filter(is_complete=True)
#         kwargs['pedidos_entregues'] = Pedido.objects.filter(is_complete=True, created_at__month=datetime.now().month).order_by('-created_at')
#         kwargs['pedidos_pendentes'] = Pedido.objects.filter(status=True)
#         kwargs['pedidos_andamento'] = Pedido.objects.filter(status=False, is_complete=False)
#         kwargs['motoristas_online'] = Motorista.objects.filter(is_online=True)
#         kwargs['motoristas_livres'] = Motorista.objects.filter(is_online=True, ocupado=False)
#         kwargs['motoristas_ocupados'] = Motorista.objects.filter(is_online=True, ocupado=True)
#         kwargs['lojas'] = Estabelecimento.objects.all().order_by('-created_at')
#         kwargs['pontos_mes'] = Ponto.objects.filter(created_at__month=now.month).order_by('bairro')
#         kwargs['pontos_all'] = Ponto.objects.all().order_by('bairro')
#         kwargs['address_all'] = Ponto.objects.all().order_by('endereco')
#         return super(DashboardMixin, self).get_context_data(**kwargs)
