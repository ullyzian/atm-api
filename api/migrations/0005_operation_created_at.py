# Generated by Django 3.0.6 on 2020-05-17 12:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200516_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
