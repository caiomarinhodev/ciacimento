# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-23 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180202_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='observacoes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
