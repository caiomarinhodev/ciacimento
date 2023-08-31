import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import ItemFormSet, ItemFormUpdateSet, FormEditCliente, FormClientAddPedido
from app.models import Pedido, Cliente, Vendedor


class UserException(Exception):
    pass


class ClientException(Exception):
    pass


class VendedorException(Exception):
    pass


class PedidoException(Exception):
    pass


class ListPedidosVendedor(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'vendedor/list_pedido_vendedor.html'
    model = Pedido
    paginate_by = 10
    context_object_name = 'pedidos_vendedor'

    def get_queryset(self):
        return Pedido.objects.filter(vendedor__user=self.request.user).order_by('-created_at')


@require_http_methods(["GET"])
def buscar_cliente(request):
    q = request.GET['q']
    qs = Cliente.objects.filter(user__username=q)
    results = []
    for cliente in qs:
        results.append({
            'id': cliente.pk,
            'nome': cliente.nome,
            'endereco': cliente.endereco,
            'numero': cliente.numero,
            'bairro': cliente.bairro,
            'cidade': cliente.cidade,
            'phone': cliente.phone,
            'email': cliente.user.email})
    return JsonResponse({'results': results})


class PedidoCreateVendedorView(LoginRequiredMixin, CreateView):
    model = Pedido
    success_url = '/app/pedidos/vendedor/'
    fields = ['valor_unitario', 'forma_pagamento', 'formato_entrega', 'prazo', 'data_entrega', 'observacoes']
    template_name = 'vendedor/add_pedido_vendedor.html'

    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(PedidoCreateVendedorView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/app/pedidos/gerente'
        return '/app/pedidos/vendedor'

    def get_context_data(self, **kwargs):
        data = super(PedidoCreateVendedorView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = FormClientAddPedido(self.request.POST)
            data['pontoset'] = ItemFormSet(self.request.POST)
        else:
            data['forms'] = FormClientAddPedido()
            data['pontoset'] = ItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pontoset = context['pontoset']
        data = self.request.POST

        try:
            cliente = self.get_or_create_client(data)
        except (UserException,):
            transaction.set_rollback(True)
            messages.error(self.request, 'Erro ao criar usuario para o cliente. Tente outro login')
            return super(PedidoCreateVendedorView, self).form_invalid(form)
        except (ClientException,):
            transaction.set_rollback(True)
            messages.error(self.request, 'Erro ao criar cliente. verifique os campos obrigatorios')
            return super(PedidoCreateVendedorView, self).form_invalid(form)

        with transaction.atomic():
            self.object = form.save()
            if pontoset.is_valid():
                pontoset.instance = self.object
                pontoset.save()
        pedido = self.object

        try:
            pedido.cliente = cliente
        except (Exception,):
            transaction.set_rollback(True)
            messages.error(self.request, 'Erro ao criar pedido.Nao foi possivel associar ao cliente')
            return super(PedidoCreateVendedorView, self).form_invalid(form)

        try:
            vendedor = Vendedor.objects.get(user=self.request.user)
            pedido.vendedor = vendedor
        except (Exception,):
            pass

        pedido.save()

        # if not self.request.user.is_superuser:
        #     users = User.objects.filter(is_superuser=True)
        #     for user in users:
        #         message = "Um novo pedido foi feito pelo vendedor " + self.request.user.first_name
        #         n = Notification(type_message='NOVO_PEDIDO_VENDEDOR', to=user, message=message)
        #         print(user)
        #         n.save()
        return super(PedidoCreateVendedorView, self).form_valid(form)

    def get_or_create_client(self, data):
        filter = Cliente.objects.filter(user__username=data['login'])
        if filter.exists():
            cliente = filter.first()
        else:
            cliente = None
        if not cliente:
            try:
                user_data = {}
                user_data['username'] = data['login']
                user_data['password'] = data['login']
                user_data['email'] = data['email']
                user_data['last_name'] = str(data['nome'])[:30]
                usuario = User.objects.create_user(**user_data)
                usuario.save()
            except (Exception,):
                raise UserException('Erro ao criar usuário para o cliente')
            try:
                cliente = Cliente(user=usuario)
                cliente.phone = data['phone']
                cliente.nome = data['nome']
                cliente.endereco = data['endereco']
                cliente.numero = data['numero']
                cliente.bairro = data['bairro']
                cliente.cidade = data['cidade']
                cliente.save()
            except (Exception,):
                raise ClientException('Erro ao criar cliente')
        return cliente


class PedidoDetailVendedorView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Pedido
    template_name = 'vendedor/view_pedido_vendedor.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            pedido = self.get_object()
            if not pedido.is_read:
                pedido.is_read = True
                pedido.save()
        return super(PedidoDetailVendedorView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(PedidoDetailVendedorView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = FormEditCliente(self.request.POST)
            data['pontoset'] = ItemFormUpdateSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            pedido = self.object
            print(pedido.cliente)
            data['forms'] = FormEditCliente(instance=pedido.cliente,
                                            initial={'nome': self.object.cliente.nome,
                                                     'email': self.object.cliente.user.email,
                                                     'phone': self.object.cliente.phone,
                                                     'endereco': self.object.cliente.endereco,
                                                     'numero': self.object.cliente.numero,
                                                     'bairro': self.object.cliente.bairro,
                                                     'cidade': self.object.cliente.cidade,
                                                     }
            )
            data['pontoset'] = ItemFormUpdateSet(instance=self.object)
        return data


class PedidoUpdateVendedorView(LoginRequiredMixin, UpdateView, ):
    model = Pedido
    success_url = '/app/pedidos/vendedor/'
    fields = ['valor_unitario', 'forma_pagamento', 'formato_entrega', 'prazo', 'data_entrega', 'entrega', 'observacoes']
    template_name = 'vendedor/edit_pedido_vendedor.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/app/pedidos/gerente'
        return '/app/pedidos/vendedor'

    def get_context_data(self, **kwargs):
        data = super(PedidoUpdateVendedorView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['forms'] = FormEditCliente(self.request.POST)
            data['pontoset'] = ItemFormUpdateSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            if self.object.cliente:
                data['forms'] = FormEditCliente(instance=self.object.cliente,
                                                initial={'nome': self.object.cliente.nome,
                                                         'email': self.object.cliente.user.email,
                                                         'phone': self.object.cliente.phone,
                                                         'endereco': self.object.cliente.endereco,
                                                         'numero': self.object.cliente.numero,
                                                         'bairro': self.object.cliente.bairro,
                                                         'cidade': self.object.cliente.cidade,
                                                         })
            data['pontoset'] = ItemFormUpdateSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pontoset = context['pontoset']
        with transaction.atomic():
            self.object = form.save()
            print(pontoset.errors)
            if pontoset.is_valid():
                pontoset.instance = self.object
                pontoset.save()
        pedido = self.object
        data = self.request.POST
        usuario = None
        cliente = None
        try:
            usuario = User.objects.get(last_name=str(data['nome'])[:30])
            usuario.email = data['email']
            usuario.save()
            cliente = usuario.cliente
        except (Exception,):
            username = 'usuario-' + str(uuid.uuid4())[:8]
            usuario = User(username=username, password='usuario', email=data['email'], last_name=str(data['nome'])[:30])
            usuario.save()
            cliente = Cliente(user=usuario)
            cliente.save()
        cliente.phone = data['phone']
        cliente.endereco = data['endereco']
        cliente.numero = data['numero']
        cliente.bairro = data['bairro']
        cliente.cidade = data['cidade']
        cliente.save()
        pedido.cliente = cliente
        pedido.save()
        # pedido = self.object
        # a = func()
        # message = "Um novo pedido foi feito pela " + self.request.user.first_name
        # for m in Motorista.objects.all():
        #     if m.is_online and not m.ocupado:
        #         n = Notification(type_message='NOVO_PEDIDO', to=m.user, message=message)
        #         n.save()
        return super(PedidoUpdateVendedorView, self).form_valid(form)
