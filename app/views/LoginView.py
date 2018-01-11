#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.views.generic import RedirectView

from app.forms import FormLogin

__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017"


class LoginView(FormView):
    """
    Displays the login form.
    """
    template_name = 'login/login.html'
    form_class = FormLogin
    # success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        print(data)
        user = authenticate(**data)
        print(user)
        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Nenhum usuário encontrado')
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        url = '/'
        try:
            user = User.objects.get(id=self.request.user.id)
        except(Exception,):
            user = None
        print(user.is_superuser)
        if user.is_superuser:
            url = '/admin/'  # Eh Gerente
        else:
            url = '/'  # Eh Vendedor
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)
