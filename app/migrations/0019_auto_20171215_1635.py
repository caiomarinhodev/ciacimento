# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-15 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20171215_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponto',
            name='observacoes',
            field=models.TextField(blank=True, null=True),
        ),
    ]