from datetime import datetime, timedelta

from django import template

from app.models import Motorista, Estabelecimento, Ponto
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
def corridas_mes(motorista):
    try:
        now = datetime.now()
        return motorista.user.pedido_set.filter(created_at__month=now.month)
    except (Motorista.DoesNotExist, Exception):
        return None


@register.filter
def corridas_hoje(motorista):
    try:
        now = datetime.now()
        return motorista.user.pedido_set.filter(created_at__day=now.day)
    except (Motorista.DoesNotExist, Exception):
        return None


@register.filter
def ganhos_mes(motorista):
    try:
        now = datetime.now()
        corridas_mes = motorista.user.pedido_set.filter(created_at__month=now.month)
        ganho_mes = 0.0
        for pedido in corridas_mes:
            ganho_mes = float(ganho_mes) + float(pedido.valor_total)
        return ganho_mes
    except (Motorista.DoesNotExist, Exception):
        return 0.0


@register.filter
def ganhos_hoje(motorista):
    try:
        now = datetime.now()
        corridas_hoje = motorista.user.pedido_set.filter(created_at__day=now.day)
        ganho_hoje = 0.0
        for pedido in corridas_hoje:
            ganho_hoje = float(ganho_hoje) + float(pedido.valor_total)
        return ganho_hoje
    except (Motorista.DoesNotExist, Exception):
        return 0.0


@register.filter
def calculate_distance(pedido):
    try:
        ptoi = pedido.ponto_set.first()
        distance = 0
        duration = 0
        for pto in pedido.ponto_set.all():
            origin = str(ptoi.lat) + "," + str(ptoi.lng)
            destin = str(pto.lat) + "," + str(pto.lng)
            calc = calculate_matrix_distance(origin, destin)
            distance = distance + int(calc['dis_value'])
            duration = duration + int(calc['dur_value'])
            ptoi = pto
        destin = str(pedido.estabelecimento.lat) + "," + str(pedido.estabelecimento.lng)
        distance = distance + int(calculate_matrix_distance(pto, destin)['dis_value'])
        duration = duration + int(calculate_matrix_distance(pto, destin)['dur_value'])
        pedido.duration = duration
        pedido.distance = distance
        pedido.save()
        return float(distance / 1000.0)
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0


@register.filter
def get_pedidos_mes(user, filter):
    now = datetime.now()
    loja = Estabelecimento.objects.get(user=user)
    try:
        return loja.pedido_set.filter(created_at__month=now.month, is_complete=True).order_by(filter)
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def get_pontos_mes(user, filter):
    now = datetime.now()
    try:
        return Ponto.objects.filter(created_at__month=now.month, pedido__estabelecimento__user=user,
                                    pedido__is_complete=True).order_by(filter)
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def get_gastos_entregas_mes(user):
    now = datetime.now()
    loja = Estabelecimento.objects.get(user=user)
    count = 0.0
    try:
        for pedido in loja.pedido_set.filter(created_at__month=now.month, is_complete=True):
            count = count + float(pedido.valor_total)
        return count
    except (ValueError, ZeroDivisionError, Exception):
        return count


@register.filter
def get_ganhos_mes(list_pedidos):
    try:
        ganho_mes = 0.0
        for pedido in list_pedidos:
            ganho_mes = float(ganho_mes) + float(pedido.valor_total)
        return ganho_mes
    except (Motorista.DoesNotExist, Exception):
        return 0.0


@register.filter
def get_renda_gerada_total(pedidos):
    count = 0.0
    try:
        for pedido in pedidos:
            count = count + float(pedido.valor_total)
        return count
    except (ValueError, ZeroDivisionError, Exception):
        return count


@register.filter
def get_renda_gerada_mes(pedidos):
    now = datetime.now()
    count = 0.0
    try:
        for pedido in pedidos.filter(created_at__month=now.month):
            count = count + float(pedido.valor_total)
        return count
    except (ValueError, ZeroDivisionError, Exception):
        return count


@register.filter
def get_init_date_period(user):
    now = datetime.now()
    try:
        start_date = now - timedelta(days=7)
        return start_date
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def get_pedidos_semana(user):
    loja = Estabelecimento.objects.get(user=user)
    now = datetime.now()
    try:
        start_date = now - timedelta(days=7)
        end_date = now
        return loja.pedido_set.filter(created_at__range=(start_date, end_date))
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def get_media_pedidos_semana(user):
    try:
        return float(len(get_pedidos_semana(user))) / 7.0
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def get_pedidos_hoje(user):
    loja = Estabelecimento.objects.get(user=user)
    now = datetime.now()
    try:
        return loja.pedido_set.filter(created_at__day=now.day)
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def get_data_grafico_seven(user):
    try:
        pedidos = get_pedidos_semana(user)
        dic = {}
        balde = []
        # for label in get_labels_grafico_seven(user):
        #     balde[label.day] = []

        for pedido in pedidos:
            if not pedido.created_at.day in dic:
                dic[pedido.created_at.day] = [pedido]
            else:
                dic[pedido.created_at.day] += [pedido]
        flag = False
        for label in get_labels_grafico_seven(user):
            for k, v in dic.items():
                if k == label.day:
                    flag = True
                    balde.append(len(v))
            if not flag:
                balde.append(0)
            else:
                flag = False
        return balde
    except Exception:
        return None


@register.filter
def get_data_anterior_grafico_seven(user):
    try:
        now = datetime.now()
        start_date = now - timedelta(days=14)
        end_date = now - timedelta(days=7)
        loja = Estabelecimento.objects.get(user=user)
        pedidos = loja.pedido_set.filter(created_at__range=(start_date, end_date))
        dic = {}
        balde = []
        arr = []
        delta = end_date - start_date
        for i in range(delta.days + 1):
            arr.append(start_date + timedelta(days=i))

        for pedido in pedidos:
            if not (pedido.created_at.day) in dic:
                dic[pedido.created_at.day] = [pedido]
            else:
                dic[pedido.created_at.day] += [pedido]
        print(dic)
        flag = False
        for label in arr:
            for k, v in dic.items():
                if k == label.day:
                    flag = True
                    balde.append(len(v))
            if not flag:
                balde.append(0)
            else:
                flag = False
        print(balde)
        return balde
    except Exception:
        return None


@register.filter
def get_labels_grafico_seven(user):
    try:
        arr = []
        now = datetime.now()
        start_date = now - timedelta(days=7)
        end_date = now
        delta = end_date - start_date
        for i in range(delta.days + 1):
            arr.append(start_date + timedelta(days=i))
        return arr
    except Exception:
        return None


@register.filter
def compara_pedidos_semana(user):
    pedidos_semana = get_pedidos_semana(user)
    loja = Estabelecimento.objects.get(user=user)
    now = datetime.now()
    try:
        start_date = now - timedelta(days=14)
        end_date = now - timedelta(days=7)
        pedidos_anterior = loja.pedido_set.filter(created_at__range=(start_date, end_date))
        value = float((100.0 * float(len(pedidos_semana))) / float(len(pedidos_anterior)))
        if value > 100.0:
            return {'signal': '+', 'x': float(value-100.0)}
        elif value == 100.0:
            return {'signal': '=', 'x': float(value-100.0)}
        return {'signal': '-', 'x': float(100.0-value)}
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def compara_ganhos_semana(user):
    ganhos_semana = get_ganhos_mes(get_pedidos_semana(user))
    loja = Estabelecimento.objects.get(user=user)
    now = datetime.now()
    try:
        start_date = now - timedelta(days=14)
        end_date = now - timedelta(days=7)
        pedidos_anterior = loja.pedido_set.filter(created_at__range=(start_date, end_date))
        ganhos_anterior = get_ganhos_mes(pedidos_anterior)
        value = float((100.0 * float(ganhos_semana)) / float(ganhos_anterior))
        if value > 100.0:
            return {'signal': '+', 'x': float(value-100.0)}
        elif value == 100.0:
            return {'signal': '=', 'x': float(value-100.0)}
        return {'signal': '-', 'x': float(100.0-value)}
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0


@register.filter
def compara_pedidos_hoje(user):
    pedidos_hoje = get_pedidos_hoje(user)
    loja = Estabelecimento.objects.get(user=user)
    now = datetime.now()
    try:
        ontem = now - timedelta(days=1)
        pedidos_ontem = loja.pedido_set.filter(created_at__day=ontem.day)
        value = float((100.0 * float(len(pedidos_hoje))) / float(len(pedidos_ontem)))
        if value > 100.0:
            return {'signal': '+', 'x': float(value-100.0)}
        elif value == 100.0:
            return {'signal': '=', 'x': float(value-100.0)}
        return {'signal': '-', 'x': float(100.0-value)}
    except (ValueError, ZeroDivisionError, Exception):
        return None


@register.filter
def compara_ganhos_hoje(user):
    ganhos_hoje = get_ganhos_mes(get_pedidos_hoje(user))
    loja = Estabelecimento.objects.get(user=user)
    now = datetime.now()
    try:
        ontem = now - timedelta(days=1)
        pedidos_ontem = loja.pedido_set.filter(created_at__day=ontem.day)
        ganhos_ontem = get_ganhos_mes(pedidos_ontem)
        value = float((100.0 * ganhos_hoje) / float(ganhos_ontem))
        if value > 100.0:
            return {'signal': '+', 'x': float(value-100.0)}
        elif value == 100.0:
            return {'signal': '=', 'x': float(value-100.0)}
        return {'signal': '-', 'x': float(100.0-value)}
    except (ValueError, ZeroDivisionError, Exception):
        return 0.0