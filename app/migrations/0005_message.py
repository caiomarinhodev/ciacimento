# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-23 15:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_auto_20171223_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Pedido')),
                ('u_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_from', to=settings.AUTH_USER_MODEL)),
                ('u_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
