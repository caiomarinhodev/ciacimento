#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import RedirectView

from app.forms import FormLogin
from app.models import Message

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

        vendedor = None
        cliente = None
        try:
            vendedor = user.vendedor
        except (Exception, ):
            pass
        try:
            cliente = user.cliente
        except (Exception, ):
            pass

        if vendedor:
            url = '/app/pedidos/vendedor'
        elif cliente:
            messages.success(self.request, 'Usuario Logado com sucesso')
            url = '/catalogo'
        else: # eh gerente
            url = '/app/pedidos/gerente'
            if user.is_superuser:
                url = '/app/pedidos/gerente'  # Eh Gerente
        return url


class LogoutView(RedirectView):
    url = '/'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def submit_message(request):
    data = request.POST
    name = data.get('name')
    message = data.get('message')
    email = data.get('email')
    try:
        objeto = Message(name=name, email=email, message=message)
        objeto.save()
        messages.success(request, 'Mensagem enviada com Sucesso!')
        return redirect('/')
    except:
        messages.error(request, 'Houve algum erro. Tente Novamente!')
        return redirect('/')
