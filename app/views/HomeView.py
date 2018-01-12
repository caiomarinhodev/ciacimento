#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from app.mixins.CustomContextMixin import CustomContextMixin

"""HomeView.py: Especifica a pagina inicial da aplicacao."""

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class HomeView(TemplateView, CustomContextMixin):
    template_name = 'site/index.html'
