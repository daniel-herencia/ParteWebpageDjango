# Generated by Django 4.0.1 on 2022-02-12 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_variablesglobales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variablesglobales',
            name='diadxt',
            field=models.BigIntegerField(default=6),
        ),
    ]
