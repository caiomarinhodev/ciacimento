# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-30 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_pedido_is_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='bairro',
            name='valor_madrugada',
            field=models.CharField(default='8', max_length=3),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
    ]
