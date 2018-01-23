from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import Pedido


class ListPedidosGerente(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'gerente/list_pedido_gerente.html'
    model = Pedido
    context_object_name = 'pedidos_gerente'

    def get_queryset(self):
        return Pedido.objects.all()
