# Generated by Django 4.2.8 on 2025-01-03 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha', models.DateTimeField()),
                ('enlace', models.URLField(blank=True, max_length=500)),
            ],
        ),
    ]
