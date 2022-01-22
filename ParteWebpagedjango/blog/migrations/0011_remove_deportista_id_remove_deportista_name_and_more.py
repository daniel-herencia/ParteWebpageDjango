# Generated by Django 4.0.1 on 2022-01-20 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_contact_name_contact_observaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='id',
        ),
        migrations.RemoveField(
            model_name='deportista',
            name='name',
        ),
        migrations.AddField(
            model_name='deportista',
            name='dxt',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='deportista',
            name='msg_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='deportista',
            name='observaciones',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='deportista',
            name='user',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='Depor',
        ),
    ]