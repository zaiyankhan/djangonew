# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-05-16 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0054_auto_20171010_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='coloredareabox',
            name='padding',
            field=models.CharField(blank=True, help_text='css padding', max_length=100, null=True),
        ),
    ]
