# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-15 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_pedido_btn_finalizado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ponto',
            old_name='descricao',
            new_name='observacoes',
        ),
    ]