# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-11-05 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formazione', '0018_auto_20180408_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='corsobase',
            name='tipo',
            field=models.CharField(blank=True, choices=[('C1', 'Corso'), ('BA', 'Corso Base')], max_length=4, verbose_name='Tipo'),
        ),
    ]
