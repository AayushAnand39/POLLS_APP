# Generated by Django 4.2.21 on 2025-06-02 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0010_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamDetails',
            fields=[
                ('examid', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('institution', models.CharField(max_length=200)),
                ('phonenumber', models.CharField(max_length=11)),
                ('numberOfQuestions', models.IntegerField(default=0)),
                ('startDate', models.DateField(default='0000-00-00')),
                ('startTime', models.TimeField(default='00:00')),
                ('endTime', models.TimeField(default='00:00')),
                ('description', models.CharField(max_length=5000)),
            ],
        ),
    ]
