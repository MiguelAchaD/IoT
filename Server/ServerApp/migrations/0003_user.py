# Generated by Django 5.1 on 2024-12-03 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServerApp', '0002_patient_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
            ],
        ),
    ]
