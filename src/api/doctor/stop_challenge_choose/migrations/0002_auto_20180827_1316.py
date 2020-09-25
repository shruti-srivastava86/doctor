# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-27 13:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stop_challenge_choose', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='stopchallengechooseassessment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stopchallengechoose',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stop_challenge_choose', to=settings.AUTH_USER_MODEL),
        ),
    ]
