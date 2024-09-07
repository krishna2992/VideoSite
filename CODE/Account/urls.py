# urls.py

from django.urls import path
from .views import *

urlpatterns = [

    path('login', custom_login, name='login'),
    path('logout', logout_view, name='logout'),
    path('home', user_home, name='home'),
    path('signup', user_signup_view, name='signup'),
    path('register/channel', channel_signup_view, name='channel_create'),
    
]