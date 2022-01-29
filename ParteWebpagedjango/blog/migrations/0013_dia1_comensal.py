# Generated by Django 4.0.1 on 2022-01-29 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dia1',
            fields=[
                ('msg_id2', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('b', models.CharField(default='-', max_length=25)),
                ('l', models.CharField(default='-', max_length=25)),
                ('d', models.CharField(default='-', max_length=25)),
                ('m', models.CharField(default='-', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Comensal',
            fields=[
                ('msg_id1', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('user', models.CharField(default='', max_length=100)),
                ('D', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='D', to='blog.dia1')),
                ('J', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='J', to='blog.dia1')),
                ('L', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='L', to='blog.dia1')),
                ('M', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='M', to='blog.dia1')),
                ('S', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='S', to='blog.dia1')),
                ('V', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='V', to='blog.dia1')),
                ('X', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='X', to='blog.dia1')),
            ],
        ),
    ]
