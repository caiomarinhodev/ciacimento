from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import FormEntrada
from app.models import Entrada


class EntradaListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Entrada
    context_object_name = 'entradas'
    template_name = 'entradas/list_entrada.html'

    def get_queryset(self):
        return Entrada.objects.all().order_by('-created_at')


class EntradaDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Entrada
    context_object_name = 'entrada'
    template_name = 'entradas/view_entrada.html'


class EntradaEditView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Entrada
    form_class = FormEntrada
    success_url = '/app/entradas'
    context_object_name = 'entrada'
    template_name = 'entradas/edit_entrada.html'


class EntradaCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Entrada
    success_url = '/app/entradas'
    form_class = FormEntrada
    template_name = 'entradas/add_entrada.html'
