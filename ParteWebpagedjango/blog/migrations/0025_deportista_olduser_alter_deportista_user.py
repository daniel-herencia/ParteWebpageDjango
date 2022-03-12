# Generated by Django 4.0.1 on 2022-03-02 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0024_alter_deportista_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportista',
            name='olduser',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='deportista',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
