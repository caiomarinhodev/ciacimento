from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import ItemFormUpdateSet, FormRegisterCliente
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
        return redirect('/registro-login', request)

    return redirect('/catalogo', request)


class RegistroClienteView(FormView):
    template_name = 'loja/registro.html'
    form_class = FormRegisterCliente
    success_url = '/catalogo'

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            user_data = {}
            user_data['username'] = data['login']
            user_data['password'] = data['senha']
            user_data['first_name'] = data['nome']
            user_data['email'] = data['email']
            usuario = User.objects.create_user(**user_data)
            usuario.save()
            user = authenticate(**user_data)
            login(self.request, user)
            cliente = Cliente(user=usuario)
            cliente.phone = data['phone']
            cliente.endereco = data['endereco']
            cliente.numero = data['numero']
            cliente.bairro = data['bairro']
            cliente.cidade = data['cidade']
            cliente.save()
            pedido = Pedido(cliente=cliente)
            pedido.save()
            self.request.session['pedido'] = pedido.id
            pedido = cliente.pedido_set.last()
            pedido.is_completed = True
            pedido.save()
            print(self.request.session['pedido'])
            # self.request.session['pedido'] = None
            # del self.request.session['pedido']
            # users = User.objects.filter(is_superuser=True)
            # for us in users:
            #     message = "Um novo pedido foi feito no Catalogo Virtual"
            #     n = Notification(type_message='NOVO_PEDIDO_LOJA', to=us, message=message)
            #     n.save()
        except (Exception,):
            return self.form_invalid(form)
        messages.success(self.request, "Cadastro realizado com sucesso")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nao foi possivel completar a acao. Tente novamente!')
        return super(RegistroClienteView, self).form_invalid(form)


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
    fields = ['valor_unitario', ]
    template_name = 'loja/carrinho.html'

    def get_success_url(self):
        return str('/')

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
        self.request.session['pedido'] = None
        del self.request.session['pedido']
        users = User.objects.filter(is_superuser=True)
        for us in users:
            message = "Um novo pedido foi feito no Catalogo Virtual"
            n = Notification(type_message='NOVO_PEDIDO_LOJA', to=us, message=message)
            n.save()
        messages.success(self.request, "Solicitacao de Orcamento realizado com sucesso")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nao foi possivel realizar o processamento do pedido. Tente novamente!')
        return super(CarrinhoView, self).form_invalid(form)
