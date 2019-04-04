# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-11 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_moderation', '0014_auto_20190315_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationRequestTreeNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('moderation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_moderation.ModerationRequest', verbose_name='moderation_request')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
