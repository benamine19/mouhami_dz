from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

AUTH_PROVIDER={'email':'email','google':'google'}
class User(AbstractUser):
  username=models.CharField( max_length=50,unique=True)
  email=models.EmailField(unique=True)
  is_admin=models.BooleanField(default=False)
  is_avocat=models.BooleanField(default=False)
  is_client=models.BooleanField(default=False)
  info=models.BooleanField(default=False)
  auth_provider=models.CharField(max_length=50 ,default=AUTH_PROVIDER.get('email'))
  USERNAME_FIELD='email'
  REQUIRED_FIELDS=['username']


class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    area = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.admin.username

class Avocat(models.Model):
    avocat = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    skills = models.TextField()
    experiences = models.TextField()
    domaines_pratique = models.TextField()
    adresse_cabinet_avocats= models.CharField(max_length=255)
    def __str__(self):
        return self.avocat.username


class Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    def __str__(self):
        return self.client.username

class Rendez_vous(models.Model):
    TIME_CHOICES = (
    ("8 AM", "8 AM"),
    ("9 AM", "9 AM"),
    ("10 AM","10 AM"),
    ("11 AM","11 AM"),
    ("1 PM","1 PM"),
    ("2 PM","2 PM"),
    ("3 PM","3 PM"),
    ("4 PM","4 PM"),
   )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    avocat = models.ForeignKey(Avocat, on_delete=models.CASCADE)
    day = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="8 PM")
    def __str__(self):
        return self.client.client.username

class Commentaire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    avocat = models.ForeignKey(Avocat, on_delete=models.CASCADE)
    description = models.TextField()
    def __str__(self):
        return self.client.client.username

