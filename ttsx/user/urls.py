from django.urls import path

from user.views import *

urlpatterns = [
    path('index/',index, name='index'),
    path('login/',login, name='login'),
    path('register/',register1, name='register'),
    path('logout/',logout, name='logout'),
    path('UserCenter/', UserCenter, name='UserCenter'),

]