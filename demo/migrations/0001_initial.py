# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sdmodel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('sdmethod', models.CharField(default=b'', max_length=100, blank=True)),
                ('table', models.TextField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
