from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name="main"

urlpatterns = [
    path('', home, name='home'),
    path('get-summary', get_summary, name='get_summary'),
    path('get-opinions', get_opinions, name='get_opinions'),
    path('get-info', get_info, name='get_info'),
    path('get-question', get_question, name='get_question'),
]