from django.urls import path

from order.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('add_order/',add_order,name='add_order'),
    path('new_order/',new_order,name='new_order')

]