# Generated by Django 4.0.1 on 2022-05-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0043_impresor_e10_impresor_e14_impresor_e20_impresor_e6_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variablesglobales',
            name='precio_e10',
            field=models.DecimalField(decimal_places=2, default=0.2, max_digits=5),
        ),
        migrations.AddField(
            model_name='variablesglobales',
            name='precio_e14',
            field=models.DecimalField(decimal_places=2, default=0.25, max_digits=5),
        ),
        migrations.AddField(
            model_name='variablesglobales',
            name='precio_e20',
            field=models.DecimalField(decimal_places=2, default=0.3, max_digits=5),
        ),
        migrations.AddField(
            model_name='variablesglobales',
            name='precio_e6',
            field=models.DecimalField(decimal_places=2, default=0.15, max_digits=5),
        ),
        migrations.AddField(
            model_name='variablesglobales',
            name='precio_tapa',
            field=models.DecimalField(decimal_places=2, default=0.4, max_digits=5),
        ),
    ]
