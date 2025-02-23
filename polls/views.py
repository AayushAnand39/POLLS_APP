from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PollCreationForm
from .models import Poll, PollOption, Vote, PollHistory
from django.contrib.auth.models import User
import random

def home(request):
    polls = list(Poll.objects.all())
    random.shuffle(polls)
    highlight_poll_id = request.GET.get('poll')
    return render(request, 'polls/home.html', {
        'polls': polls,
        'highlight_poll_id': highlight_poll_id,
    })

def about(request):
    return render(request, 'polls/about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'polls/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def create_poll(request):
    if request.method == 'POST':
        form = PollCreationForm(request.POST)
        if form.is_valid():
            poll = Poll.objects.create(
                creator_username=request.user.username,
                question=form.cleaned_data['question']
            )
            options = []
            for field in ['option1', 'option2', 'option3', 'option4']:
                text = form.cleaned_data.get(field)
                if text:
                    option = PollOption.objects.create(poll=poll, option_text=text)
                    options.append(option)
            PollHistory.objects.create(
                user=request.user,
                poll_id=poll.id,
                action='created'
            )
            messages.success(request, "Poll created successfully!")
            return redirect('home')
    else:
        form = PollCreationForm()
    return render(request, 'polls/create_poll.html', {'form': form})

@login_required
def user_profile(request):
    profile = request.user.profile
    histories = PollHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'polls/user_profile.html', {
        'profile': profile,
        'histories': histories,
    })

def vote(request, poll_id, option_id):
    poll = get_object_or_404(Poll, id=poll_id)
    option = get_object_or_404(PollOption, id=option_id, poll=poll)
    if request.user.is_authenticated:
        Vote.objects.create(
            poll=poll,
            option=option,
            voter_username=request.user.username
        )
        option.votes += 1
        option.save()
        PollHistory.objects.create(
            user=request.user,
            poll_id=poll.id,
            action='reacted'
        )
        messages.success(request, "Your vote has been recorded!")
    else:
        messages.error(request, "You must be logged in to vote.")
    return redirect('home')