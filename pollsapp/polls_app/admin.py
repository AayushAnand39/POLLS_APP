from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Messages)
admin.site.register(models.ExamDetails)
admin.site.register(models.ExamQuestions)
admin.site.register(models.ExamResults)
admin.site.register(models.ExamResponse)
admin.site.register(models.PollQuestions)
admin.site.register(models.PollResponses)