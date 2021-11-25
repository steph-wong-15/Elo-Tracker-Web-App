# Generated by Django 3.2.8 on 2021-11-24 08:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_delete_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.match')),
            ],
        ),
    ]