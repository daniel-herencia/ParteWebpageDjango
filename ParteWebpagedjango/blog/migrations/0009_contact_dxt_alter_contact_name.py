# Generated by Django 4.0.1 on 2022-01-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_contact_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='dxt',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=1),
        ),
    ]