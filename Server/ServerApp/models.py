from django.db import models

class Endpoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    method = models.TextField()
    url = models.TextField()

class Api(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    baseUrl = models.TextField()
    headers = models.JSONField
    endpoints = models.ForeignKey(to=Endpoint, on_delete=models.CASCADE)

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    public_id = models.TextField()
    name = models.TextField()
    age = models.IntegerField()
    status = models.TextField()