# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_moderation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderation_collections', to='djangocms_moderation.Workflow', verbose_name='workflow')),
            ],
        ),
        migrations.RemoveField(
            model_name='moderationrequest',
            name='workflow',
        ),
        migrations.AddField(
            model_name='moderationrequest',
            name='collection',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='moderation_requests', to='djangocms_moderation.ModerationCollection'),
            preserve_default=False,
        ),
    ]