# Generated by Django 2.2.5 on 2020-04-29 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secret',
            name='lifetime',
            field=models.CharField(max_length=10000, verbose_name='Время жизни секрета'),
        ),
    ]
