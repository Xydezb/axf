import random
import time

from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from carts.models import ShoppingCart
from goods.models import Goods
from order.form import addressForm
from order.models import UserAddress, OrderInfo, OrderGoods
from user.models import User

from utils.functions import session_login


# @session_login
def index(request):
    if request.method == 'GET':
        user_address = UserAddress.objects.all()
        # print(user_address)
        return render(request, 'user_center_site.html',{'add': user_address})
    if request.method == 'POST':
        form = addressForm(request.POST)
        if form.is_valid():
            #输入正确
            filename = form.cleaned_data['filename']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            number = form.cleaned_data['number']
            UserAddress.objects.create(user=filename, address=address, signer_postcode=zipcode, signer_mobile=number)

            return HttpResponseRedirect(reverse('order:index'))
        errors = form.errors
        return render(request,'user_center_site.html',{'errors':errors})

# 订单页面
def add_order(request):
    if request.method == 'GET':
        id = request.session['user_id']
        # 取到订单多个对象
        order = OrderInfo.objects.filter(user_id=id).all()
        # 给一个空列表
        orders = []
        # 循环对象，i代表每个对象
        for i in order:
            # 让对象变成字典格式
            order_dict = dict(model_to_dict(i))

            # 商品详情order字段关联的订单模型里的对象
            order_dict['A'] = OrderGoods.objects.filter(order=i).all()
            orders.append(order_dict)

        print(orders)
        return render(request, 'user_center_order.html',{'orders':orders})

#添加订单
def new_order(request):
    if request.method == 'POST':
        # 拿到登录用户id
        id = request.session['user_id']
        # 从用户表里拿到id一样的对象
        user = User.objects.filter(id=id).first()
        print(user)
        # 前端传的总价钱
        price= float(request.POST.get('price')[:-1])
        print(price)
        # 从购物车里拿到用户id跟登陆用户id是一样的所有商品id
        good_id = ShoppingCart.objects.filter(user_id=id).all()
        # print(good_id)

        # 唯一订单数
        a = time.time()
        a = str(a*1000000)
        b = a[7:-2]
        #收货地址
        # print(id)
        address = UserAddress.objects.filter(id=id).first()
        # print(address)

        ordes = OrderInfo()
        ordes.user = user
        ordes.order_sn = b
        ordes.order_mount = price
        ordes.address = address.address
        ordes.signer_name = address.user
        ordes.signer_mobile = address.signer_mobile
        ordes.save()

        show = OrderInfo.objects.filter(order_sn=b,user=user).first()
        # print(good_id)
        for i in good_id:
            # print(i.id)
            ordes_goods = OrderGoods()
            ordes_goods.order = show
            ordes_goods.goods = Goods.objects.filter(id=i.goods_id).first()
            ordes_goods.goods_nums = i.nums
            ordes_goods.save()

        # 订单保存成功，删除购物车里的商品
        ShoppingCart.objects.filter(is_select=1).delete()

        return JsonResponse({'code': 200})