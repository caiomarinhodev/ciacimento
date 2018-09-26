from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models import Cliente, Vendedor


class ClientesGerenteListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Cliente
    paginate_by = 10
    context_object_name = 'clientes'
    template_name = 'clientes/list_clientes.html'

    def get_queryset(self):
        return Cliente.objects.all().order_by('-created_at')


class ClientesVendedorListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Cliente
    paginate_by = 10
    context_object_name = 'clientes'
    template_name = 'clientes/list_clientes.html'

    def get_queryset(self):
        vendedor = Vendedor.objects.get(user=self.request.user)
        return Cliente.objects.filter(pedido__vendedor=vendedor).order_by('-created_at')
