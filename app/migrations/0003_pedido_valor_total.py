# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pedido_nome_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='valor_total',
            field=models.CharField(default=0.0, max_length=6),
            preserve_default=False,
        ),
    ]