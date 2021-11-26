# Generated by Django 3.2.8 on 2021-11-26 08:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stats', '0011_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='admins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
