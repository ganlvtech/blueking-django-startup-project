# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.CharField(default=b'', max_length=128)),
                ('user_info', models.CharField(default=b'', max_length=255)),
                ('path', models.CharField(default=b'', max_length=1024)),
                ('method', models.CharField(default=b'', max_length=20)),
                ('ip', models.CharField(default=b'', max_length=40)),
                ('user_agent', models.CharField(default=b'', max_length=1024)),
                ('query', models.CharField(default=b'', max_length=1024)),
                ('body', models.CharField(default=b'', max_length=4096)),
                ('response_code', models.IntegerField(default=0)),
                ('response_length', models.IntegerField(default=0)),
                ('response_body', models.CharField(default=b'', max_length=4096)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
