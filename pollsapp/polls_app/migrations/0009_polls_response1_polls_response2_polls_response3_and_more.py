# Generated by Django 4.2.21 on 2025-05-20 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0008_remove_polls_authorname_polls_authoremail'),
    ]

    operations = [
        migrations.AddField(
            model_name='polls',
            name='response1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='polls',
            name='response2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='polls',
            name='response3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='polls',
            name='response4',
            field=models.IntegerField(default=0),
        ),
    ]
