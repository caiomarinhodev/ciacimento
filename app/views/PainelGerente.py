from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import Pedido


class ListPedidosGerente(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'gerente/list_pedido_gerente.html'
    model = Pedido
    paginate_by = 10
    context_object_name = 'pedidos_gerente'

    def get_queryset(self):
        return Pedido.objects.all().order_by('-created_at')


class ListPedidosMesGerente(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'gerente/list_pedido_gerente.html'
    model = Pedido
    paginate_by = 10
    context_object_name = 'pedidos_gerente'

    def get_queryset(self):
        now = datetime.now()
        return Pedido.objects.filter(created_at__month=now.month, created_at__year=now.year)


class ListPedidosSemanaGerente(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'gerente/list_pedido_gerente.html'
    model = Pedido
    paginate_by = 10
    context_object_name = 'pedidos_gerente'

    def get_queryset(self):
        now = datetime.now()
        start_date = now - timedelta(days=6)
        end_date = now
        return Pedido.objects.filter(created_at__range=(start_date, end_date))


class ListPedidosHojeGerente(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'gerente/list_pedido_gerente.html'
    model = Pedido
    paginate_by = 10
    context_object_name = 'pedidos_gerente'

    def get_queryset(self):
        now = datetime.now()
        month = datetime.now().month
        year = datetime.now().year
        return Pedido.objects.filter(created_at__day=now.day, created_at__month=month, created_at__year=year)
