# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-11-22 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0049_auto_20181028_1639'),
        ('formazione', '0027_auto_20181120_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='lezionecorsobase',
            name='docente',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='anagrafica.Persona', verbose_name='Docente della lezione'),
        ),
        migrations.AddField(
            model_name='lezionecorsobase',
            name='obiettivo',
            field=models.CharField(default='', max_length=128, null=True, verbose_name='Obiettivo formativo della lezione'),
        ),
    ]
