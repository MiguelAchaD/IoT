# Generated by Django 5.1 on 2025-01-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServerApp', '0002_reunion'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='reunions',
            field=models.ManyToManyField(to='ServerApp.reunion'),
        ),
    ]