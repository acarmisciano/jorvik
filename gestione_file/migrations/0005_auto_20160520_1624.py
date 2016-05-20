# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-20 16:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestione_file', '0004_immagine_downloads'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documento',
            options={'verbose_name': 'documento', 'verbose_name_plural': 'documenti'},
        ),
        migrations.AlterModelOptions(
            name='documentosegmento',
            options={'verbose_name': 'segmento', 'verbose_name_plural': 'segmenti'},
        ),
        migrations.AlterModelOptions(
            name='immagine',
            options={'verbose_name': 'immagine', 'verbose_name_plural': 'immagini'},
        ),
        migrations.AddField(
            model_name='documento',
            name='data_pubblicazione',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data pubblicazione'),
        ),
        migrations.AddField(
            model_name='immagine',
            name='data_pubblicazione',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data pubblicazione'),
        ),
        migrations.AlterField(
            model_name='documentosegmento',
            name='titolo',
            field=models.ForeignKey(blank=True, help_text="Usato solo con il segmento 'Volontari aventi un dato titolo'", null=True, on_delete=django.db.models.deletion.CASCADE, to='curriculum.Titolo'),
        ),
    ]
