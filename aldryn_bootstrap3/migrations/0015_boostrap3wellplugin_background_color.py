# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-20 18:51
from __future__ import unicode_literals

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_bootstrap3', '0014_translations_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='boostrap3wellplugin',
            name='background_color',
            field=colorfield.fields.ColorField(blank=True, max_length=18, null=True),
        ),
    ]
