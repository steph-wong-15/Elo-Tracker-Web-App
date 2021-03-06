# Generated by Django 3.2.8 on 2021-12-07 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stats', '0016_auto_20211207_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcoming',
            name='participant_A',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant_A', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='upcoming',
            name='participant_B',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant_B', to=settings.AUTH_USER_MODEL),
        ),
    ]
