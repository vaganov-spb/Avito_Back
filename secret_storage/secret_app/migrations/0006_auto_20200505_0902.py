# Generated by Django 2.2.5 on 2020-05-05 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_app', '0005_auto_20200504_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secret',
            name='secret_word',
            field=models.CharField(max_length=128, verbose_name='Кодовая Фраза'),
        ),
    ]
