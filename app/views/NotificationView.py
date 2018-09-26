from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from app.models import Notification
from app.views.snippet_template import render_block_to_string


class NotificacoesListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Notification
    paginate_by = 10
    context_object_name = 'notificacoes'
    template_name = 'notificacoes/list_notificacoes.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            for n in Notification.objects.filter(to=self.request.user):
                n.is_read = True
                n.save()
        return Notification.objects.all().order_by('-created_at')


@require_http_methods(["GET"])
def notificar_novo_pedido_vendedor(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='NOVO_PEDIDO_VENDEDOR',
                                              is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)


@require_http_methods(["GET"])
def notificar_novo_pedido_loja(request):
    notificacao = Notification.objects.filter(to=request.user, type_message='NOVO_PEDIDO_LOJA',
                                              is_read=False).last()
    context = Context({'notificacao': notificacao, 'user': request.user})
    return_str = render_block_to_string('includes/notificacao.html', context)
    if notificacao:
        notificacao.is_read = True
        notificacao.save()
    return HttpResponse(return_str)
