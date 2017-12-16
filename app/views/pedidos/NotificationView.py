#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from app.models import Notification
from app.views.snippet_template import render_block_to_string
from app.mixins.CustomContextMixin import CustomContextMixin


class NotificacoesListView(LoginRequiredMixin, ListView, CustomContextMixin):
    login_url = '/login/'
    model = Notification
    context_object_name = 'notificacoes'
    template_name = 'notificacoes/list_notificacoes.html'

    def get_queryset(self):
        for n in Notification.objects.filter(to=self.request.user):
            n.is_read=True
            n.save()
        return Notification.objects.filter(to=self.request.user).order_by('-created_at')


@require_http_methods(["GET"])
def notificar_novo_pedido_motorista(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='NOVO_PEDIDO', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_delete_loja_motorista(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='DELETE_LOJA', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_accept_order_loja(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='ACCEPT_ORDER', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)
    

@require_http_methods(["GET"])
def notificar_all_delivered_loja(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='ALL_DELIVERED', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)



@require_http_methods(["GET"])
def notificar_enable_rota_motorista(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='ENABLE_ROTA', is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)
