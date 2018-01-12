# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from app.views.geocoding import geocode


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class BaseAddress(models.Model):
    class Meta:
        abstract = True

    bairro = models.CharField(max_length=200, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name='Endereço')
    numero = models.CharField(max_length=5, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ponto de Referência')
    lat = models.CharField(max_length=100, blank=True, null=True)
    lng = models.CharField(max_length=100, blank=True, null=True)


class Usuario(TimeStamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_gerente = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.user)


class Cliente(TimeStamped, BaseAddress):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # cpf = models.CharField(max_length=100, blank=True, null=True, default="")
    nome = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Telefone')
    full_address = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            self.full_address = address
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        super(Cliente, self).save(*args, **kwargs)


class Categoria(TimeStamped):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.nome)


class Tipo(TimeStamped):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.nome)


class Marca(TimeStamped):
    nome = models.CharField(max_length=100)
    site = models.URLField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    foto = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.nome)


class Produto(TimeStamped):
    cod = models.CharField(max_length=50)
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(Tipo, blank=True, null=True, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)
    cor = models.CharField(max_length=100, blank=True, null=True)
    peso = models.CharField(max_length=50, blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, blank=True, null=True)
    valor = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_oferta = models.BooleanField(default=False)
    descricao = models.TextField(blank=True, null=True)
    instrucoes = models.TextField(blank=True, null=True)
    tipo_embalagem = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.marca)


class Pedido(TimeStamped):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # USER
    valor_total = models.CharField(max_length=100, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s' % (self.cliente, self.valor_total)

    def save(self, *args, **kwargs):
        try:
            valor = 0.00
            for it in self.item_set.all():
                if it.valor_item:
                    it.valor_item = valor + float(it.valor_item)
            self.valor_total = valor
        except (Exception,):
            pass
        super(Pedido, self).save(*args, **kwargs)


class Foto(TimeStamped):
    url = models.URLField(null=True, blank=True)
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.url)


class Item(TimeStamped):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.CharField(max_length=100)
    valor_item = models.CharField(max_length=100, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s - %s' % (self.produto, self.quantidade)

    def save(self, *args, **kwargs):
        try:
            valor = 0.00
            if self.produto.valor:
                self.valor_item = float(self.produto.valor) * float(self.quantidade)
            else:
                self.valor_item = valor
        except (Exception, ):
            pass
        super(Item, self).save(*args, **kwargs)


type_notification = (
    ('NOVO_PEDIDO_LOJA', 'NOVO_PEDIDO_LOJA'),
    ('NOVO_PEDIDO_VENDEDOR', 'NOVO_PEDIDO_VENDEDOR'),
)


class Notification(TimeStamped):
    message = models.TextField()
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    type_message = models.CharField(choices=type_notification, max_length=100)
    is_read = models.BooleanField(default=False)


class Message(models.Model):
    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.email)
