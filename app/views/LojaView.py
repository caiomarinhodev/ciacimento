from django.views.generic import DetailView
from django.views.generic import ListView

from app.models import Produto


class ListProducts(ListView):
    template_name = 'loja/loja.html'
    model = Produto
    context_object_name = 'produtos'
    ordering = '-created_at'
    queryset = Produto.objects.all()


class ProductDetail(DetailView):
    model = Produto
    context_object_name = 'produto'
    template_name = 'loja/produto.html'