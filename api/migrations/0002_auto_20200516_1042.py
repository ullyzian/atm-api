# Generated by Django 3.0.6 on 2020-05-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='kind',
            field=models.CharField(choices=[('C', 'Credit'), ('D', 'Debit')], max_length=1),
        ),
    ]
