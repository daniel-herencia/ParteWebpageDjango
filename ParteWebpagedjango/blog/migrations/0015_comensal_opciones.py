# Generated by Django 4.0.1 on 2022-01-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_dia1_b_alter_dia1_d_alter_dia1_l_alter_dia1_m'),
    ]

    operations = [
        migrations.AddField(
            model_name='comensal',
            name='opciones',
            field=models.CharField(default='', max_length=25),
        ),
    ]