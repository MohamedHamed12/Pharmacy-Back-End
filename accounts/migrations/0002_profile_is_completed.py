# Generated by Django 4.2.6 on 2024-01-18 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
