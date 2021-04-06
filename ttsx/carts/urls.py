from django.urls import path

from carts.views import *

urlpatterns = [
    path('index/', index,name='index'),
    path('add_cart/', add_cart, name='add_cart'),
    path('place_order/', place_order,name='place_order'),
    path('change_cart/',change_cart,name='change_cart')


]