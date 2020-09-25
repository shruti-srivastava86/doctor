# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-27 13:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sleep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sleepdailyassessment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sleep_daily_assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sleepassessment',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sleep_assessment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='sleepdailyassessment',
            index=models.Index(fields=['assessment_date'], name='sleep_sleep_assessm_87a5f4_idx'),
        ),
        migrations.AddIndex(
            model_name='sleepassessment',
            index=models.Index(fields=['calculation_weight'], name='sleep_sleep_calcula_1077e3_idx'),
        ),
    ]
