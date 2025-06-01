from django.db import models
from django.utils import timezone
import random

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, primary_key=True, unique=True)
    phonenumber = models.CharField(max_length=11)
    password = models.CharField(max_length=500)
    logintime = models.DateTimeField(default=timezone.now)
    logouttime = models.DateTimeField(default=timezone.now)
    
class Polls(models.Model):
    questionnumber = models.BigAutoField(primary_key=True)
    authoremail = models.EmailField(max_length=200, default="example@email.com")
    question = models.CharField(max_length=5000)
    option1 = models.CharField(max_length=200)
    response1 = models.IntegerField(default=0)
    option2 = models.CharField(max_length=200)
    response2 = models.IntegerField(default=0)
    option3 = models.CharField(max_length=200)
    response3 = models.IntegerField(default=0)
    option4 = models.CharField(max_length=200)
    response4 = models.IntegerField(default=0)

class Messages(models.Model):
    messageid = models.BigAutoField(primary_key=True)
    senderemail = models.EmailField(max_length=200)
    receiveremail = models.EmailField(max_length=200)
    message = models.CharField(max_length=5000)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    

    