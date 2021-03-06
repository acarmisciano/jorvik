# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-03-15 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ufficio_soci', '0016_auto_20190314_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportelenco',
            name='report_type',
            field=models.CharField(blank=True, choices=[('vol', 'Volontari'), ('vog', 'Volontari Giovani'), ('ivcm', 'IV e CM'), ('dim', 'Dimessi'), ('vir', 'Volontari in Riserva'), ('tra', 'Trasferiti'), ('dip', 'Dipendenti'), ('soc', 'Soci Ordinari'), ('est', 'Volontari Estesi/In Estensione'), ('sag', 'Soci al giorno'), ('sos', 'Sostenitori'), ('exs', 'Ex Sostenitori'), ('stu', 'Volontari con zero turni'), ('ele', 'Elettorato'), ('tit', 'Soci per Titoli'), ('gen', 'Generico')], max_length=5, null=True),
        ),
    ]
