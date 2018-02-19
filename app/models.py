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


class Cliente(TimeStamped, BaseAddress):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Telefone')
    full_address = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.numero = str(self.numero).replace('_', '')
        self.phone = str(self.phone).replace('_', '')
        try:
            address = self.endereco + ", " + self.numero + ",Campina Grande,PB"
            self.full_address = address
            pto = geocode(address)
            self.lat = pto['latitude']
            self.lng = pto['longitude']
        except (Exception,):
            pass
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s - %s - %s/PB' % (self.user.first_name, self.phone, self.cidade)


class Vendedor(TimeStamped, BaseAddress):
    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Telefone')
    full_address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.user.first_name)


class Categoria(TimeStamped):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.nome)

    def __str__(self):
        return u'%s' % (self.nome)


class Tipo(TimeStamped):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.nome)

    def __str__(self):
        return u'%s' % (self.nome)


class Marca(TimeStamped):
    nome = models.CharField(max_length=100)
    site = models.URLField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    foto = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.nome)

    def __str__(self):
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

    def __str__(self):
        return u'%s - %s' % (self.nome, self.marca)


type_entrega = (
    ('COM DESCARREGO', 'COM DESCARREGO'),
    ('SEM DESCARREGO', 'SEM DESCARREGO')
)


class FormaPagamento(TimeStamped):
    forma = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.forma)

    def __unicode__(self):
        return '%s' % self.forma


class Pedido(TimeStamped):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)  # USER
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, blank=True, null=True)
    formato_entrega = models.CharField(max_length=100, blank=True, null=True, choices=type_entrega)
    data_entrega = models.DateField(blank=True, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True)
    valor_unitario = models.CharField(max_length=100, blank=True, null=True)
    prazo = models.CharField(max_length=300, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    entrega = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.cliente)

    def __str__(self):
        return u'%s' % (self.cliente)

    def save(self, *args, **kwargs):
        self.valor_unitario = str(self.valor_unitario).replace(',', '.')
        super(Pedido, self).save(*args, **kwargs)


class Foto(TimeStamped):
    url = models.URLField(null=True, blank=True)
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.url)

    def __str__(self):
        return u'%s' % (self.url)


class Item(TimeStamped):
    class Meta:
        verbose_name = 'Iten'
        verbose_name_plural = 'Itens'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.CharField(max_length=100)
    valor_item = models.CharField(max_length=100, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s - %s' % (self.produto, self.quantidade)

    def __str__(self):
        return u'%s - %s' % (self.produto, self.quantidade)

    def save(self, *args, **kwargs):
        try:
            valor = 0.00
            if self.produto.valor:
                self.valor_item = float(self.produto.valor) * float(self.quantidade)
            else:
                self.valor_item = valor
            self.pedido.save()
        except (Exception,):
            pass
        super(Item, self).save(*args, **kwargs)


type_notification = (
    ('NOVO_PEDIDO_LOJA', 'NOVO_PEDIDO_LOJA'),
    ('NOVO_PEDIDO_VENDEDOR', 'NOVO_PEDIDO_VENDEDOR'),
)


class Notification(TimeStamped):
    class Meta:
        verbose_name = 'Notificacao'
        verbose_name_plural = 'Notificacoes'

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


colors = (
    ('#001F3F', 'NAVY'),
    ('#3c8dbc', 'AZUL'),
    ('#00c0ef', 'AZUL-CLARO'),
    ('#39CCCC', 'TURQUESA'),
    ('#00a65a', 'VERDE'),
    ('#605ca8', 'ROXO'),
    ('#f39c12', 'AMARELO'),
    ('#ff851b', 'LARANJA'),
    ('#f56954', 'VERMELHO'),
    ('#D81B60', 'ROSA'),
    ('#d2d6de', 'CINZA'),
    ('#111111', 'PRETO'),
)


class Entrada(TimeStamped):
    cliente = models.CharField(max_length=300, blank=True, null=True)
    id_pedido = models.CharField(max_length=100, blank=True, null=True)
    valor_total = models.CharField(max_length=100, blank=True, null=True)
    valor_pago = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    cor = models.CharField(max_length=100, blank=True, null=True, choices=colors)

    def __str__(self):
        return str(self.id_pedido)

    def __unicode__(self):
        return '%s' % self.cliente

    def save(self, *args, **kwargs):
        self.valor_total = str(self.valor_total).replace(',', '.')
        self.valor_pago = str(self.valor_pago).replace(',', '.')
        super(Pedido, self).save(*args, **kwargs)


class Saida(TimeStamped):
    eminente = models.CharField(max_length=300, blank=True, null=True)
    razao = models.CharField(max_length=300, blank=True, null=True)
    valor = models.CharField(max_length=300, blank=True, null=True)
    forma = models.ForeignKey(FormaPagamento, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    cor = models.CharField(max_length=100, blank=True, null=True, choices=colors)

    def save(self, *args, **kwargs):
        self.valor = str(self.valor).replace(',', '.')
        super(Pedido, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.eminente

    def __str__(self):
        return str(self.id_pedido)
