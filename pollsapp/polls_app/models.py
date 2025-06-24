from django.db import models
from django.utils import timezone
import random
from datetime import date, time

# Create your models here.
class User(models.Model):
    name         = models.CharField(max_length=200)
    username     = models.CharField(max_length=200)
    email        = models.EmailField(max_length=200, primary_key=True, unique=True)
    phonenumber  = models.CharField(max_length=11)
    password     = models.CharField(max_length=500)
    logintime    = models.DateTimeField(default=timezone.now)
    logouttime   = models.DateTimeField(default=timezone.now)
    profile_pic  = models.ImageField(
                     upload_to="profiles/",
                     null=True,
                     blank=True,
                     help_text="Optional profile picture"
                   )

class PollQuestions(models.Model):
    questionid = models.BigAutoField(primary_key=True)
    authoremail = models.EmailField(max_length=200, default="example@email.com")
    pollDescription = models.CharField(max_length=5000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
                upload_to="profiles/",
                null=True,
                blank=True,
                help_text="Optional picture for the poll question"
            )

class PollResponses(models.Model):
    optionid = models.BigAutoField(primary_key=True)
    questionid = models.IntegerField(default=0)
    optionDescription = models.CharField(max_length=5000)
    response = models.IntegerField(default=0)
    image = models.ImageField(
                upload_to="profiles/",
                null=True,
                blank=True,
                help_text="Optional picture for the poll response"
            )

class Messages(models.Model):
    messageid = models.BigAutoField(primary_key=True)
    senderemail = models.EmailField(max_length=200)
    receiveremail = models.EmailField(max_length=200)
    message = models.CharField(max_length=5000)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    
class ExamDetails(models.Model):
    examid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    institution = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=11)
    numberOfQuestions = models.IntegerField(default=0)
    startDate = models.DateField(default=date.today)
    startTime = models.TimeField(default=time(0, 0))
    endTime = models.TimeField(default=time(0, 0))
    description = models.CharField(max_length=5000)

class ExamQuestions(models.Model):
    questionid = models.BigAutoField(primary_key=True)
    questionnumber = models.IntegerField(default=0)
    examid = models.IntegerField(default=0)
    question = models.CharField(max_length=5000)
    option1 = models.CharField(max_length=5000)
    option2 = models.CharField(max_length=5000)
    option3 = models.CharField(max_length=5000)
    option4 = models.CharField(max_length=5000)
    positiveScore = models.IntegerField(default=0)
    negativeScore = models.IntegerField(default=0)
    correctOption = models.IntegerField(default=0)
    explanation = models.CharField(max_length=5000, null=True, blank=True)

class ExamResults(models.Model):
    resultid = models.BigAutoField(primary_key=True)
    examid = models.IntegerField(default=0)
    email = models.EmailField(max_length=200)
    score = models.IntegerField(default=0)
    timeTaken = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)

class ExamResponse(models.Model):
    responseid = models.BigAutoField(primary_key=True)
    examid = models.IntegerField(default=0)
    email = models.EmailField(max_length=200)
    questionid = models.IntegerField(default=0)
    response = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)