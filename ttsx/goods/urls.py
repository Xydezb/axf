from django.urls import path

from goods.views import *

urlpatterns = [
    path('goodlist/', goodlist, name='goodlist'),
    path('detail/', detail, name='detail'),
]