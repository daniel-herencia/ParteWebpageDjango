# Generated by Django 4.0.1 on 2023-06-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_variablesglobales_precio_e10_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportista',
            name='tipo',
            field=models.CharField(default='B', max_length=1),
        ),
    ]