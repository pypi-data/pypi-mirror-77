# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacc', '0006_account_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='number',
            field=models.IntegerField(blank=True, db_index=True, default=None, null=True, verbose_name='invoice number'),
        ),
    ]
