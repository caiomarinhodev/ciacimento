#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import DashboardMixin

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class HomeView(TemplateView):
    template_name = 'site/index.html'
