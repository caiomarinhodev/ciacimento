from datetime import datetime, timedelta

from django import template

from app.models import Pedido
from app.views.geocoding import calculate_matrix_distance

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return float(float(value) / float(arg))
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def soma_avaliacao(value):
    try:
        sum = 0.0
        for c in value:
            sum = float(sum) + float(c.nota)
        return float(float(sum) / float(len(value)))
    except (ValueError, ZeroDivisionError):
        return "Nao Avaliado"


@register.filter
def get_latitude(motorista):
    try:
        return motorista.user.location_set.all().order_by('-created_at').last().lat
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0


@register.filter
def get_longitude(motorista):
    try:
        return motorista.user.location_set.all().order_by('-created_at').last().lng
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0


@register.filter
def pedidos_vendedor_hoje(user):
    try:
        now = datetime.now()
        return Pedido.objects.filter(vendedor__user=user, created_at__day=now.day)
    except (Exception,):
        return None


@register.filter
def pedidos_vendedor_semana(user):
    try:
        now = datetime.now()
        start_date = now - timedelta(days=6)
        end_date = now
        return Pedido.objects.filter(vendedor__user=user, created_at__range=(start_date, end_date))
    except (Exception,):
        return None


@register.filter
def pedidos_vendedor_mes(user):
    try:
        now = datetime.now()
        return Pedido.objects.filter(vendedor__user=user, created_at__month=now.month)
    except (Exception,):
        return None


@register.filter
def pedidos_vendedor_total(user):
    try:
        return Pedido.objects.filter(vendedor__user=user)
    except (Exception,):
        return None


@register.filter
def pedidos_hoje(user):
    try:
        now = datetime.now()
        return Pedido.objects.filter(created_at__day=now.day)
    except (Exception,):
        return None


@register.filter
def pedidos_semana(user):
    try:
        now = datetime.now()
        start_date = now - timedelta(days=6)
        end_date = now
        return Pedido.objects.filter(created_at__range=(start_date, end_date))
    except (Exception,):
        return None


@register.filter
def pedidos_mes(user):
    try:
        now = datetime.now()
        return Pedido.objects.filter(created_at__month=now.month)
    except (Exception,):
        return None


@register.filter
def pedidos_total(user):
    try:
        return Pedido.objects.all()
    except (Exception,):
        return None


@register.filter
def quatidades_hoje(user):
    try:
        now = datetime.now()
        list_pedidos = Pedido.objects.filter(created_at__day=now.day)
        qtd = 0
        for pedido in list_pedidos:
            for item in pedido.item_set.all():
                qtd = qtd + int(item.quantidade)
        return qtd
    except (Exception,):
        return None


@register.filter
def quatidades_semana(user):
    try:
        now = datetime.now()
        start_date = now - timedelta(days=6)
        end_date = now
        list_pedidos = Pedido.objects.filter(created_at__range=(start_date, end_date))
        qtd = 0
        for pedido in list_pedidos:
            for item in pedido.item_set.all():
                qtd += int(item.quantidade)
        return qtd
    except (Exception,):
        return None


@register.filter
def quatidades_mes(user):
    try:
        now = datetime.now()
        list_pedidos = Pedido.objects.filter(created_at__month=now.month, created_at__year=now.year)
        qtd = 0
        for pedido in list_pedidos:
            for item in pedido.item_set.all():
                qtd += int(item.quantidade)
        return qtd
    except (Exception,):
        return None
