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
from datetime import datetime
from django.conf import settings
from django.forms.models import model_to_dict

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
    if user.logintime != user.logouttime:
        return redirect("login")

    questionsList = models.Polls.objects.all()
    questionsData = []

    for question in questionsList:
        # look up the author User
        try:
            author = models.User.objects.get(email=question.authoremail)
            author_name  = author.name
            # if they have uploaded a photo, use it; otherwise use a static fallback
            if author.profile_pic:
                author_photo = author.profile_pic.url
            else:
                author_photo = settings.STATIC_URL + "img/anonymous.png"
        except models.User.DoesNotExist:
            author_name  = "Unknown"
            author_photo = settings.STATIC_URL + "img/anonymous.png"

        # compute percentages as before
        total = (
            question.response1 +
            question.response2 +
            question.response3 +
            question.response4
        ) or 1
        pct1 = (question.response1 * 100) / total
        pct2 = (question.response2 * 100) / total
        pct3 = (question.response3 * 100) / total
        pct4 = (question.response4 * 100) / total

        questionsData.append({
            "questionnumber": question.questionnumber,
            "author_name":    author_name,
            "author_photo":   author_photo,
            "question":       question.question,
            "option1":        question.option1,
            "option2":        question.option2,
            "option3":        question.option3,
            "option4":        question.option4,
            "percentage1":    pct1,
            "percentage2":    pct2,
            "percentage3":    pct3,
            "percentage4":    pct4,
        })

    return render(request, "dashboard.html", {
        "name":          user.name,
        "email":         email,
        "username":      user.username,
        "phonenumber":   user.phonenumber,
        "message":       "Login successful",
        "questionsData": questionsData,
    })
    
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
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    qn = int(data.get("questionnumber"))
    opt = int(data.get("optionnumber"))
    poll = models.Polls.objects.get(questionnumber=qn)

    if   opt == 1: poll.response1 += 1
    elif opt == 2: poll.response2 += 1
    elif opt == 3: poll.response3 += 1
    elif opt == 4: poll.response4 += 1
    poll.save()

    # recompute percentages
    total = poll.response1 + poll.response2 + poll.response3 + poll.response4 or 1
    p1 = round(poll.response1 * 100 / total, 1)
    p2 = round(poll.response2 * 100 / total, 1)
    p3 = round(poll.response3 * 100 / total, 1)
    p4 = round(poll.response4 * 100 / total, 1)

    return JsonResponse({
        "message": "Vote recorded!",
        "percentages": {
            "1": p1,
            "2": p2,
            "3": p3,
            "4": p4
        }
    })

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
    for msg in completeUserHistory:
        other_email = msg.receiveremail if msg.senderemail == email else msg.senderemail
        if other_email not in recent:
            recent[other_email] = msg

    recentChatsData = []
    for other_email, msg in recent.items():
        # look up the other user
        try:
            other = models.User.objects.get(email=other_email)
            name = other.name
            photo = other.profile_pic.url if other.profile_pic else settings.STATIC_URL + "img/anonymous.png"
        except models.User.DoesNotExist:
            name, photo = "Unknown", settings.STATIC_URL + "img/anonymous.png"

        recentChatsData.append({
            "email":     other_email,
            "name":      name,
            "photo_url": photo,
            "message":   msg.message,
            "time":      msg.time.strftime("%Y-%m-%d %H:%M:%S"),
            "read":      msg.read,
        })

    return render(request, "chat.html", {
        "email":           email,
        "recentChatsData": recentChatsData,
    })

@csrf_exempt
def chat_search(request):
    if request.method != "POST":
        return JsonResponse({"error":"Invalid request"}, status=400)

    data = json.loads(request.body)
    prefix = data.get("name","").strip()
    # prefix‐match on name
    users = models.User.objects.filter(name__istartswith=prefix)[:10]

    results = []
    for u in users:
        results.append({
            "email":     u.email,
            "name":      u.name,
            "photo_url": u.profile_pic.url if u.profile_pic else settings.STATIC_URL + "img/anonymous.png"
        })
    return JsonResponse({"results": results})

    
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

def sendData(request):
    if request.method == "POST":
        data = json.loads(request.body).get("formData")
        date_str = data.get("date")
        start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        details = models.ExamDetails(name = data.get("name"), email = data.get("email"), institution = data.get("institution"), phonenumber = data.get("phonenumber"), numberOfQuestions = data.get("number"), startDate = start_date, startTime = data.get("starttime"), endTime = data.get("endtime"), description = data.get("description"))
        details.save()
        examid = models.ExamDetails.objects.filter(email = data.get("email")).order_by("-examid").first().examid
        print(examid)
        print(data)
        return JsonResponse({"message" : "Data received successfully", "data" : data, "examid" : examid}, status=200)
    else:
        return JsonResponse({"error": "error"}, status=400)
    
@csrf_exempt
def sendExamQuestion(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    payload = json.loads(request.body)
    examid         = payload.get("examid")
    questionnumber = payload.get("questionnumber")
    data           = payload.get("formData", {})
    pk             = payload.get("pk")  # may be None

    # If the client already told us which PK to update, use it:
    if pk:
        try:
            eq = models.ExamQuestions.objects.get(pk=pk, examid=examid)
        except models.ExamQuestions.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)
    else:
        # Otherwise try to find an existing one by examid+questionnumber:
        eq, created = models.ExamQuestions.objects.get_or_create(
            examid=examid,
            questionnumber=questionnumber,
            defaults={}
        )

    # Now update all fields from incoming data:
    eq.question      = data.get("question",      eq.question)
    eq.option1       = data.get("option1",       eq.option1)
    eq.option2       = data.get("option2",       eq.option2)
    eq.option3       = data.get("option3",       eq.option3)
    eq.option4       = data.get("option4",       eq.option4)
    eq.positiveScore = data.get("positive",      eq.positiveScore)
    eq.negativeScore = data.get("negative",      eq.negativeScore)
    eq.correctOption = data.get("correct",       eq.correctOption)
    eq.save()

    return JsonResponse({
        "message":        "Question saved successfully",
        "examid":         examid,
        "questionnumber": questionnumber,
        "pk":             eq.pk
    }, status=200)

    
def attendexam(request, email):
    user = models.User.objects.get(email = email)
    if user.logintime == user.logouttime:
        return render(request,"attendexam.html",{"email":email})
    else:
        return render(request,"Login.html")
    
def loadExam(request):
    if request.method == "POST":
        examid = json.loads(request.body).get("examid")
        examdetails = models.ExamDetails.objects.get(examid = examid)
        examDetails = model_to_dict(examdetails)
        examquestiondetails = models.ExamQuestions.objects.filter(examid = examid).order_by("questionnumber")
        examquestions = []
        for details in examquestiondetails:
            examquestions.append({
                "questionnumber" : details.questionnumber,
                "question" : details.question,
                "option1" : details.option1,
                "option2" : details.option2,
                "option3" : details.option3,
                "option4" : details.option4,
                "positive" : details.positiveScore,
                "negative" : details.negativeScore,
                "correctoption" : details.correctOption
            })
        return JsonResponse({"message" : "Questions loaded successfully", "examquestions" : examquestions, "examid" : examid, "examdetails" : examDetails}, status=200)
    else:
        return JsonResponse({"error": "error"}, status=400) 
    

@csrf_exempt
def get_exam_meta(request):
    """
    Returns: {
      examid, name, startDate, startTime, endTime, numberOfQuestions
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    data      = json.loads(request.body)
    examid    = data.get("examid")
    try:
        details = models.ExamDetails.objects.get(examid=examid)
    except models.ExamDetails.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    # Serialize only what you need
    return JsonResponse({
        "examid":           details.examid,
        "name":             details.name,
        "startDate":        details.startDate.isoformat(),
        "startTime":        details.startTime.strftime("%H:%M:%S"),
        "endTime":          details.endTime.strftime("%H:%M:%S"),
        "numberOfQuestions": details.numberOfQuestions,
    })


@csrf_exempt
def submit_exam(request):
    """
    Expects JSON:
    {
      examid: 123,
      email: "stu@example.com",
      responses: [
         { questionnumber: 1, selectedOption: 2, timestamp: "2025-06-22T14:05:30" },
         ...
      ],
      timeTakenSeconds: 3600
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid"}, status=400)

    payload = json.loads(request.body)
    examid  = payload["examid"]
    email   = payload["email"]
    resp_list = payload["responses"]
    time_taken = payload["timeTakenSeconds"]

    # Compute score & counts
    correct = wrong = total_score = 0

    for r in resp_list:
        qn = r["questionnumber"]
        sel = r["selectedOption"]
        # Save each response
        models.ExamResponse.objects.create(
            examid=examid,
            email=email,
            questionid=qn,
            response=sel
        )
        # Score it
        eq = models.ExamQuestions.objects.get(examid=examid, questionnumber=qn)
        if sel == eq.correctOption:
            correct += 1
            total_score += eq.positiveScore
        else:
            wrong += 1
            total_score += eq.negativeScore

    # Save the aggregate result
    models.ExamResults.objects.create(
        examid=examid,
        email=email,
        score=total_score,
        timeTaken=time_taken,
        correctAnswers=correct,
        wrongAnswers=wrong
    )

    return JsonResponse({
        "status": "ok",
        "score": total_score,
        "correct": correct,
        "wrong": wrong
    })

    
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