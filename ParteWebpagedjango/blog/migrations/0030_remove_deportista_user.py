# Generated by Django 4.0.1 on 2022-03-02 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_remove_deportista_user1_deportista_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='user',
        ),
    ]
