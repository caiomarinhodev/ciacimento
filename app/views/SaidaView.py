from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from app.forms import FormSaida
from app.models import Saida


class SaidaListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Saida
    paginate_by = 10
    context_object_name = 'saidas'
    template_name = 'saidas/list_saida.html'

    def get_queryset(self):
        return Saida.objects.all().order_by('-created_at')


class SaidaDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Saida
    context_object_name = 'saida'
    template_name = 'saidas/view_saida.html'


class SaidaEditView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Saida
    success_url = '/app/saidas'
    form_class = FormSaida
    context_object_name = 'saida'
    template_name = 'saidas/edit_saida.html'


class SaidaCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Saida
    success_url = '/app/saidas'
    form_class = FormSaida
    template_name = 'saidas/add_saida.html'
