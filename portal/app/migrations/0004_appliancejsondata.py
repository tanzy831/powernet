# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-16 14:30
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20171005_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplianceJsonData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devices_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'appliance_data',
            },
        ),
    ]
