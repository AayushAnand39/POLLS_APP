from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Polls)
admin.site.register(models.Messages)
admin.site.register(models.ExamDetails)
admin.site.register(models.ExamQuestions)