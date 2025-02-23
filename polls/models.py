from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class PollHistory(models.Model):
    ACTION_CHOICES = (
        ('created', 'Created'),
        ('reacted', 'Reacted'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll_id = models.IntegerField()  
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} poll {self.poll_id}"

class Poll(models.Model):
    creator_username = models.CharField(max_length=150)
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.option_text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    voter_username = models.CharField(max_length=150)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter_username} voted on {self.poll.question}"