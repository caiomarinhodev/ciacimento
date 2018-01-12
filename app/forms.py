#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, inlineformset_factory

from app.models import Pedido, Item, Cliente, Marca, Produto


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone'
            if field_name == 'numero' or field_name == 'number':
                field.widget.attrs['class'] = 'form-control numero'


class FormBaseAddress(BaseForm):
    cep = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'required': True,
                                                                       'maxlength': 200,
                                                                       'placeholder': 'CEP'
                                                                       }))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    bairro = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                          'maxlength': 200,
                                                                          'placeholder': 'Bairro'
                                                                          }))
    cidade = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 100,
                                                                           'placeholder': 'Cidade'
                                                                           }))


class FormLogin(BaseForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))


# class FormPedido(ModelForm, BaseForm):
#     class Meta:
#         model = Pedido
#         fields = []


class FormItem(ModelForm, BaseForm):
    class Meta:
        model = Item
        fields = ['produto', 'quantidade', ]


class FormEditItem(ModelForm, BaseForm):
    class Meta:
        model = Item
        fields = ['produto', 'quantidade', ]


class FormRegister(ModelForm, BaseForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                               'maxlength': 200,
                                                               'placeholder': 'Nome Estabelecimento'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                             'maxlength': 200,
                                                             'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True,
                                                                 'placeholder': 'Senha'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    cep = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'required': True,
                                                                       'maxlength': 200,
                                                                       'placeholder': 'CEP'
                                                                       }))
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': True,
                                                                             'maxlength': 200,
                                                                             'placeholder': 'Endereço'
                                                                             }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    bairro = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 100,
                                                                           'placeholder': 'Bairro'
                                                                           }))

    class Meta:
        model = Cliente
        fields = []


class FormEditCliente(ModelForm, BaseForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                         'maxlength': 200,
                                                         'placeholder': 'Nome Completo'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    endereco = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                            'maxlength': 200,
                                                                            'placeholder': 'Endereço'
                                                                            }))
    numero = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'required': True,
                                                                         'maxlength': 200,
                                                                         'placeholder': 'Número'
                                                                         }))
    bairro = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'required': True,
                                                                           'maxlength': 100,
                                                                           'placeholder': 'Bairro'
                                                                           }))
    cidade = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': True,
                                                                          'maxlength': 200,
                                                                          'placeholder': 'Cidade'
                                                                          }))

    email = forms.EmailField()

    class Meta:
        model = Cliente
        fields = []


class FormMarca(ModelForm, BaseForm):
    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'required': False, 'placeholder': 'Logotipo do Estabelecimento'
                                                         }))

    class Meta:
        model = Marca
        fields = ['site', 'nome', 'descricao', ]


class FormProduto(ModelForm, BaseForm):
    class Meta:
        model = Produto
        fields = ['cod', 'nome', 'categoria', 'cor', 'peso', 'marca', 'valor', 'is_oferta', 'descricao', 'instrucoes',
                  'tipo_embalagem', ]


class FormPedido(FormBaseAddress):
    nome = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                         'maxlength': 200,
                                                         'placeholder': 'Nome Estabelecimento'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'maxlength': 200,
                                                          'placeholder': 'Telefone'}))
    email = forms.EmailField()


ItemFormSet = inlineformset_factory(Pedido, Item, form=FormItem, extra=1)

ItemFormUpdateSet = inlineformset_factory(Pedido, Item, form=FormEditItem, extra=0)
