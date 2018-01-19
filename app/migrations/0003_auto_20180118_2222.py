# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-18 22:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180116_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('forma', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='valor_entrega',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='valor_total',
        ),
        migrations.AddField(
            model_name='pedido',
            name='data_entrega',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='formato_entrega',
            field=models.CharField(blank=True, choices=[('COM DESCARREGO', 'COM DESCARREGO'), ('SEM DESCARREGO', 'SEM DESCARREGO')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='prazo',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='valor_unitario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='forma_pagamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.FormaPagamento'),
        ),
    ]
