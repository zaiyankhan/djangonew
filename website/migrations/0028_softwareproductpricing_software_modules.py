# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-16 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0027_auto_20170513_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwareproductpricing',
            name='software_modules',
            field=models.ManyToManyField(related_name='pricings', to='website.SoftwareModule'),
        ),
    ]
