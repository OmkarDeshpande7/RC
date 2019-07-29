from django.urls import path,re_path
from . import views

from django.views.generic import DetailView
from django.contrib.auth import authenticate,login , logout

urlpatterns = [

    path('display/', views.display),
    path('', views.home),
    path('rules', views.rules),
    path('login/', views.logged),
    path('logout/', logout, {'template_name': 'Result.html'}),
    path('register/',views.register, name='register'),
    path('anscheck/',views.anscheck, name='anscheck'),
    path('timer/', views.timer),
    path('validate_username/', views.validate_username),
    path('score/', views.score_chart , name = 'score_chart'),
    #re_path(r'/',logout, {'template_name': 'reg_form.html'}),
    re_path(r'/',views.url),
]
