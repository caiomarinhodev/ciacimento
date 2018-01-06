#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import DashboardMixin
from app.models import ConfigAdmin

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class AppView(TemplateView):
    template_name = 'page/index.html'


class CollectView(TemplateView):
    template_name = 'page/collect.html'


class ContributeView(TemplateView):
    template_name = 'page/contribute.html'


class DashboardView(LoginRequiredMixin, TemplateView, DashboardMixin):
    login_url = '/login/'
    template_name = 'admin/dashboard.html'


def set_feriado_admin(request):
    config = ConfigAdmin.objects.first()
    config.is_feriado = not config.is_feriado
    config.save()
    return redirect('/dashboard')
