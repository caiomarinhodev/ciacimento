# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='nome_cliente',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]