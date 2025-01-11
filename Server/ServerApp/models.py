from django.db import models
import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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

class Reunion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    url = models.URLField(max_length=500, blank=True)

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    public_id = models.TextField()
    name = models.TextField()
    age = models.IntegerField()
    sex = models.TextField()
    city = models.TextField()
    status = models.TextField()
    record_history = models.ForeignKey(to=History, on_delete=models.CASCADE, null=True, blank=True)
    reunions = models.ManyToManyField(to=Reunion, blank=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    patients = models.ManyToManyField(to=Patient)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username