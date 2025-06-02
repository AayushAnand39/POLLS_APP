from django.shortcuts import render, redirect
from . import models
from django.utils import timezone
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from collections import OrderedDict
import urllib.parse
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        setpassword = request.POST.get('setpassword')
        resetpassword = request.POST.get('resetpassword')
        if (setpassword!=resetpassword):
            return render(request,"register.html",{"message":"Invalid credentials. Check your registration once again"})
        else:
            user = models.User(name = name, username = username, email = email, phonenumber = phonenumber, password = setpassword)
            user.save()
            return render(request,"register.html",{"message":"Registration successful. Please proceed to login"})
    else:
        return render(request,"register.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = models.User.objects.get(email=email, username=username, password=password)
        if user:
            user.logintime = timezone.now()
            user.logouttime = timezone.now()
            user.save()
            safe_email = urllib.parse.quote(email)
            return redirect(f"dashboard/{safe_email}")
        else:
            return render(request,"Login.html",{"message" : "Invalid credentials"})
    else:
        return render(request,"Login.html")
    
def dashboard(request, email):
    email = urllib.parse.unquote(email)
    user = models.User.objects.get(email=email)
    if user.logintime == user.logouttime:
        questionsList = models.Polls.objects.all()
        questionsData = []
        for question in questionsList:
            response1 = question.response1
            response2 = question.response2
            response3 = question.response3
            response4 = question.response4
            completeResponse = response1+response2+response3+response4
            percentage1 = 0
            percentage2 = 0
            percentage3 = 0
            percentage4 = 0
            if completeResponse == 0:
                percentage1 = 0
                percentage2 = 0
                percentage3 = 0
                percentage4 = 0
            else:
                percentage1 = (response1*100)/(completeResponse)
                percentage2 = (response2*100)/(completeResponse)
                percentage3 = (response3*100)/(completeResponse)
                percentage4 = (response4*100)/(completeResponse)
            questionsData.append({
                "questionnumber": question.questionnumber,
                "question":question.question,
                "authoremail":question.authoremail,
                "option1":question.option1,
                "option2":question.option2,
                "option3":question.option3,
                "option4":question.option4,
                "response1":question.response1,
                "response2":question.response2,
                "response3":question.response3,
                "response4":question.response4,
                "percentage1":percentage1,
                "percentage2":percentage2,
                "percentage3":percentage3,
                "percentage4":percentage4
            })
        return render(request,"dashboard.html",{"name" : user.name, "email": email, "username": user.username, "phonenumber": user.phonenumber, "message":"Login successful", "questionsData":questionsData})
    else:
        return redirect("login")
    
def post(request, email):
    email = urllib.parse.unquote(email)
    user = models.User.objects.get(email=email)
    if user.logintime == user.logouttime:
        if request.method == "POST":
            question = request.POST.get('question')
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            questionPost = models.Polls(authoremail=email, question=question, option1=option1, option2=option2, option3=option3, option4=option4)
            questionPost.save()
            return render(request,"post.html",{"name" : user.name, "email": email, "username": user.username, "phonenumber": user.phonenumber, "message":"Login successful"})
        else:
            return render(request,"post.html",{"name" : user.name, "email": email, "username": user.username, "phonenumber": user.phonenumber, "message":"Login successful"})
    else:
        return redirect("login")
    
@csrf_exempt
def vote(request):
    if request.method == "POST":
        data = json.loads(request.body)
        questionnumber = int(data.get("questionnumber"))
        optionnumber = int(data.get("optionnumber"))
        question = models.Polls.objects.get(questionnumber = questionnumber)
        if optionnumber == 1:
            question.response1 += 1
        elif optionnumber == 2:
            question.response2 += 1
        elif optionnumber == 3:
            question.response3 += 1
        elif optionnumber == 4:
            question.response4 += 1
        question.save()
        return JsonResponse({"message": "Vote recorded!"})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

def chat(request, email):
    email = urllib.parse.unquote(email)
    user  = models.User.objects.get(email=email)
    if user.logintime != user.logouttime:
        return redirect("login")
    completeUserHistory = (
        models.Messages.objects
        .filter(Q(senderemail=email) | Q(receiveremail=email))
        .order_by('-time')
    )
    recent = OrderedDict()
    for userHistory in completeUserHistory:
        other = userHistory.receiveremail if userHistory.senderemail == email else userHistory.senderemail
        if other not in recent:
            recent[other] = userHistory
    recentChatsData = []
    for other, userHistory in recent.items():
        recentChatsData.append({
            "other":   other,
            "message": userHistory.message,
            "time":    userHistory.time.strftime("%Y-%m-%d %H:%M:%S"),
            "read":    userHistory.read,
        })

    return render(request, "chat.html", {
        "name":            user.name,
        "email":           email,
        "username":        user.username,
        "phonenumber":     user.phonenumber,
        "message":         "Login successful",
        "recentChatsData": recentChatsData,
    })

@csrf_exempt
def chat_search(request):
    if request.method == "POST":
        data = json.loads(request.body)
        search_name = data.get("name", "")
        users = models.User.objects.filter(name__icontains=search_name)[:10]
        results = [{"email": user.email, "name": user.name} for user in users]
        return JsonResponse({'results': results})
    
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        senderemail = data.get("senderEmail")
        receiveremail = data.get("receiverEmail")
        message = data.get("message")
        if not receiveremail or not senderemail:
            return JsonResponse({"error": "Missing sender or receiver email"}, status=400)
        messagePost = models.Messages(senderemail=senderemail, receiveremail=receiveremail, message=message, time=timezone.now(), read=False)
        messagePost.save()
        return JsonResponse({"status": "Message sent"})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def get_chats(request):
    if request.method == "POST":
        data = json.loads(request.body)
        senderEmail = data.get("senderEmail")
        receiverEmail = data.get("receiverEmail")
        if not senderEmail or not receiverEmail:
            return JsonResponse({"error": "Missing sender or receiver email"}, status=400)
        messages = models.Messages.objects.filter(senderemail=senderEmail, receiveremail=receiverEmail) | models.Messages.objects.filter(senderemail=receiverEmail, receiveremail=senderEmail)
        messages = messages.order_by('time')
        messages_data = []
        for message in messages:
            messages_data.append({
                "senderemail": message.senderemail,
                "receiveremail": message.receiveremail,
                "message": message.message,
                "time": message.time.strftime("%Y-%m-%d %H:%M:%S"),
                "read": message.read
            })
        return JsonResponse({"messages": messages_data})
    return JsonResponse({"error": "Invalid request"}, status=400)

def official(request, email):
    user = models.User.objects.get(email=email)
    if user.logintime == user.logouttime:
        return render(request,"official.html",{"email": email, "message" : "Welcome to the official section of the polls app"})
    else:
        return render(request,"Login.html")
    
def createexam(request, email):
    user = models.User.objects.get(email = email)
    if user.logintime == user.logouttime:
        return render(request,"createexam.html",{"email":email})
    else:
        return render(request,"Login.html")

    
def logout(request, email):
    email = urllib.parse.unquote(email)
    user = models.User.objects.get(email = email)
    print(email)
    if user:
        user.logouttime = timezone.now()
        user.save()
        print("Successfully Logged Out")
        return redirect("index")
    else:
        print("Session ended")
        return redirect("index")