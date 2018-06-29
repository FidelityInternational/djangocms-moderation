# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-20 07:13
from __future__ import unicode_literals

from django.db import migrations
from djangocms_moderation.utils import generate_compliance_number


def populate_reference_number(apps, schema_editor):
    PageModerationRequest = apps.get_model('djangocms_moderation', 'PageModerationRequest')

    for moderation_request in PageModerationRequest.objects.all():
        ref_number = generate_compliance_number(moderation_request.workflow.reference_number_backend)
        moderation_request.reference_number = ref_number
        moderation_request.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_moderation', '0002_auto_20180420_0811'),
    ]

    operations = [
        migrations.RunPython(populate_reference_number, migrations.RunPython.noop,),
    ]
