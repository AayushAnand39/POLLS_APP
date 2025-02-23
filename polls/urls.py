from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_poll/', views.create_poll, name='create_poll'),
    path('profile/', views.user_profile, name='user_profile'),
    path('vote/<int:poll_id>/<int:option_id>/', views.vote, name='vote'),
]