from django.contrib import admin

from app.models import *

"""
admin.py: Definicao de classes para gerenciar no painel de admin do Django.
"""
__author__ = "Caio Marinho"
__copyright__ = "Copyright 2017, LES-UFCG"


class FotoInline(admin.TabularInline):
    model = Foto


class ItemInline(admin.TabularInline):
    model = Item


class FotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'produto',)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'full_address', 'created_at')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id', 'created_at')


class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id', 'site', 'foto', 'created_at')


class ProdutoAdmin(admin.ModelAdmin):
    inlines = [
        FotoInline,
    ]
    list_display = ('cod', 'nome', 'categoria', 'cor', 'peso', 'marca', 'valor', 'tipo_embalagem',
                    'is_active', 'is_oferta',
                    'created_at')


class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]
    list_display = ('cliente', 'valor_total', 'created_at')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'quantidade', 'valor_item', 'pedido', 'created_at')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'type_message', 'to', 'is_read')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'email',)


class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id',)


class VendedorAdmin(admin.ModelAdmin):
    list_display = ('user', 'id',)


admin.site.register(Foto, FotoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Vendedor, VendedorAdmin)