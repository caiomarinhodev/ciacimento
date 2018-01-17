import uuid

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import ItemFormUpdateSet, FormEditCliente
from app.mixins.CustomContextMixin import CustomContextMixin
from app.models import Produto, Categoria, Pedido, Cliente, Item, Notification


class ListProducts(ListView, CustomContextMixin):
    template_name = 'loja/loja.html'
    model = Produto
    context_object_name = 'produtos'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        kwargs['categorias'] = Categoria.objects.all()
        return super(ListProducts, self).get_context_data(**kwargs)

    def get_queryset(self):
        categoria = ""
        tipo = ""
        if 'categoria' in self.request.GET:
            categoria = str(self.request.GET['categoria'])
        if 'tipo' in self.request.GET:
            tipo = str(self.request.GET['tipo'])
        qs = Produto.objects.all()
        if categoria != "":
            qs = Produto.objects.filter(categoria=categoria)
        elif tipo != "":
            qs = Produto.objects.filter(tipo=tipo)
        return qs


class ProductDetail(DetailView, CustomContextMixin):
    model = Produto
    context_object_name = 'produto'
    template_name = 'loja/produto.html'

    def get_context_data(self, **kwargs):
        kwargs['categorias'] = Categoria.objects.all()
        return super(ProductDetail, self).get_context_data(**kwargs)


def add_item_carrinho(request, id_produto):
    if 'pedido' in request.session:
        item = Item(produto_id=id_produto, quantidade=1, pedido_id=request.session['pedido'])
        item.save()
        messages.success(request, 'Item adicionado com sucesso')
    else:
        username = 'usuario-' + str(uuid.uuid4())[:8]
        usuario = User(username=username, password='usuario')
        usuario.save()
        cliente = Cliente(user=usuario)
        cliente.save()
        pedido = Pedido(cliente=cliente)
        pedido.save()
        item = Item(produto_id=id_produto, quantidade=1, pedido=pedido)
        item.save()
        request.session['pedido'] = pedido.id
        messages.success(request, 'Item adicionado com sucesso')
    return redirect('/catalogo', request)


def remove_item_carrinho(request, id_item, id_pedido):
    try:
        item = Item.objects.get(id=id_item, pedido_id=id_pedido)
        item.delete()
        messages.success(request, 'Item deletado com sucesso')
    except (Exception,):
        messages.error(request, 'Nao foi possivel deletar')
    return redirect('/catalogo', request)


class CarrinhoView(UpdateView):
    model = Pedido
    context_object_name = 'pedido'
    fields = ['valor_total', ]
    template_name = 'loja/carrinho.html'

    def get_success_url(self):
        pedido = self.get_object()
        return str('/checkout/') + str(pedido.cliente.id)

    def get_context_data(self, **kwargs):
        data = super(CarrinhoView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pontoset'] = ItemFormUpdateSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
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
        return super(CarrinhoView, self).form_valid(form)


class ProcessPedidoView(UpdateView, CustomContextMixin):
    model = Cliente
    form_class = FormEditCliente
    template_name = 'loja/process_pedido_one.html'
    success_url = '/'

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            cliente = self.get_object()
            cliente = Cliente.objects.get(id=cliente.pk)
            usuario = cliente.user
            usuario.first_name = data['nome']
            cliente.phone = data['phone']
            usuario.email = data['email']
            cliente.endereco = data['endereco']
            cliente.numero = data['numero']
            cliente.bairro = data['bairro']
            cliente.cidade = data['cidade']
            usuario.save()
            cliente.save()
            pedido = cliente.pedido_set.last()
            pedido.is_completed = True
            pedido.save()
            self.request.session['pedido'] = None
            del self.request.session['pedido']
            users = User.objects.filter(is_superuser=True)
            for us in users:
                message = "Um novo pedido foi feito no Catalogo Virtual"
                n = Notification(type_message='NOVO_PEDIDO_LOJA', to=us, message=message)
                n.save()
        except (Exception,):
            return self.form_invalid(form)
        messages.success(self.request, "Pedido realizado com sucesso")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nao foi possivel realizar o processamento do pedido. Tente novamente!')
        return super(ProcessPedidoView, self).form_invalid(form)
