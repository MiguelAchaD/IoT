from django.db import models
import random

class Endpoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    method = models.TextField()
    url = models.TextField()

class Api(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    base_url = models.TextField()
    headers = models.JSONField()
    endpoints = models.ManyToManyField(to=Endpoint)

class Key(models.Model):
    id = models.AutoField(primary_key=True)
    key_value = models.TextField()

class ApiKeys(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.TextField(unique=True)
    key = models.ForeignKey(to=Key, on_delete=models.CASCADE)

    def get_random_key(self):
        # Obtén todas las claves relacionadas con esta API y elige una al azar.
        keys = Key.objects.filter(apikeys=self)
        return random.choice(keys).key_value if keys else None

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    heart_rate = models.FloatField()
    ambient_temperature = models.FloatField()
    xyz_accelerometer = models.TextField()
    is_exposed_to_light = models.BooleanField()

class History(models.Model):
    id = models.AutoField(primary_key=True)
    day_of_record = models.DateField()
    records = models.ManyToManyField(to=Record)

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    public_id = models.TextField()
    name = models.TextField()
    age = models.IntegerField()
    sex = models.TextField()
    status = models.TextField()
    record_history = models.ForeignKey(to=History, on_delete=models.CASCADE, null=True, blank=True)
