from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name = "index"),
    path("register",views.register,name = "register"),
    path("login",views.login,name = "login"),
    path("dashboard/<str:email>",views.dashboard,name="dashboard"),
    path("post/<str:email>",views.post,name="post"),
    path("logout/<str:email>",views.logout,name="logout"),
    path("vote/", views.vote, name="vote"),
    path("chat/<str:email>",views.chat,name="chat"),
    path("chat-search/",views.chat_search,name="chat-search"),
    path("send-message/",views.send_message,name="send-message"),
    path("get-chats/",views.get_chats,name="get-chats"),
    path("official/<str:email>",views.official,name="official"),
    path("createexam/<str:email>",views.createexam,name="createexam"),
    path("send-data/",views.sendData,name="send-data"),
    path("send-exam-question/",views.sendExamQuestion,name="send-exam-question"),
    path("attendexam/<str:email>",views.attendexam,name="attendexam"),
    path("load-exam/",views.loadExam,name="loadExam"),
    path("submit-exam/",views.submit_exam,name="submitExam"),
    path("get-exam-meta/",views.get_exam_meta,name="get-exam-meta"),
    # path("liveleaderboard/<str:email>",views.liveleaderboard,name="liveleaderboard"),
    path(
        'liveleaderboard/<str:email>/',
        views.liveleaderboard_page,
        name='liveleaderboard'
    ),

    # Serves JSON data for AJAX
    path(
        'liveleaderboard-data/<str:email>/',
        views.liveleaderboard_data,
        name='liveleaderboard-data'
    ),
]
