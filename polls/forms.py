from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Poll, PollOption

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'age', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile =  user.profile if hasattr(user, 'profile') else None
            from .models import Profile
            Profile.objects.create(user=user, age=self.cleaned_data['age'])
        return user

class PollCreationForm(forms.Form):
    question = forms.CharField(max_length=255, label="Poll Question")
    option1 = forms.CharField(max_length=255, label="Option 1")
    option2 = forms.CharField(max_length=255, label="Option 2")
    option3 = forms.CharField(max_length=255, label="Option 3", required=False)
    option4 = forms.CharField(max_length=255, label="Option 4", required=False)