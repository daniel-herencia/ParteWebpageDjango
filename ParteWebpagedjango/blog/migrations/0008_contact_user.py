# Generated by Django 4.0.1 on 2022-01-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_contact_desc_remove_contact_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.CharField(default='', max_length=100),
        ),
    ]
