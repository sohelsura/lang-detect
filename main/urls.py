from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name="main"

urlpatterns = [
    path('get_news_summary/', get_news_summary, name='get_news_summary'),
]