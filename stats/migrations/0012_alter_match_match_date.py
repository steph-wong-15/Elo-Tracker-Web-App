# Generated by Django 3.2.8 on 2021-11-25 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]