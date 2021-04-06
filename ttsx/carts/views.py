from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from carts.models import ShoppingCart
from goods.models import Goods
from order.models import UserAddress
from ttsx.settings import DATABASES
from utils.functions import session_login


# @session_login
# 购物车首页                                       try：不报错执行  exce：报错执行
def index(request):
    if request.method == 'GET':
        try:
            #取得到user说明登陆了，取不到会报错
            user = request.session['user_id']
            # 取到购物车表里用户的购物车数据
            cart = ShoppingCart.objects.filter(user_id=user).all()
            # 返回，传去一个对象
            return render(request, 'cart.html', {'cart': cart})
        except:
                # 没登陆   给一个空字典
                f_goods={}
                # 取到session里保存的商品数据 实际就是商品的 id 和 数量
                goods = request.session.get('goods')

                try:
                    # 如果session里没有商品数据，那么下面的循环语句就会报不可迭代错误，
                    for i in goods:
                        # print(i)    goods={商品id：商品数量, 。。。。}
                        # 遍历取到goods的键，goods[i]取到值， Goods.objects.filter(id=i)从商品表里拿到跟id一样的对象
                        # 往f_goods空字典里添加数据， 以对象做键，goods[i]做值， 字典键不存在添加，存在修改值
                        f_goods[Goods.objects.filter(id=i)]=goods[i]
                except:
                    pass
        return render(request, 'cart.html',{'f_goods': f_goods})

    if request.method == 'POST':
        id = request.POST.get('goods_id')
        try:
            user = request.session['user_id']
            print(id,user)
            # 删除
            ShoppingCart.objects.filter(goods_id=id,user_id=user).delete()
            return JsonResponse({'code': 200})
        except:
            goods = request.session.get('goods')
            # request.session['goods_id'] = goods
            # print(request.session['goods_id'])
            goods.pop(id)
            request.session['goods_id'] = goods
            return JsonResponse({'code': 200})
            # print(request.session['goods_id'])



def add_cart(request):
    if request.method == 'POST':
        #获取到前端ajax传过来的两个值  id：商品id   num：商品数量
        id = request.POST.get('goods_id')
        num = int(request.POST.get('goods_num'))
        # print(id)
        # print(num)
        # 查看是否登录，登录购物车加数据库，没登录session
        try:
            # 直接获取session 登录id， 如果获取不到，报错执行except，获取的到，代表登陆，执行try
            user =request.session['user_id']
            print(user)
            # TRUNCATE TABLE f_shopping_cart  表自增空从1开始的sql语句
            cart = ShoppingCart.objects.filter(goods_id=id).first()
            if cart:
                ShoppingCart.objects.filter(user_id=user,goods_id=id).update(nums=num)
            if not cart:
                ShoppingCart.objects.create(nums=num, goods_id=id, user_id=user)
            #状态码返回，前端接受状态码来进行下一步操作
            return JsonResponse({'code': 200})
        except:
            # 没登陆
            try:
                # 参数 goods 获取到商品存的session值，获取不到报错执行except，其次往下执行
                goods =dict(request.session.get('goods'))
                # 判定前端传过来的商品id 存不存在商品的session值里，存在就修改数量， 商品的session值我们存的是一个字典{商品id：商品数量}
                # 存在：
                if id in goods:
                    goods[id] += num
                    request.session['goods'] = goods

                # 不存在：  不存在就添加一个字典，不会覆盖之前的，  update  。然后重新定义session缓存
                else:
                    goods.update({id:num})
                    request.session['goods'] = goods
                return JsonResponse({'code': 400})


            except:
                #  获取不到session  往session缓存里保存商品数据
                request.session['goods'] = {id:num}
                return JsonResponse({'code': 400})


def change_cart(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        num = int(request.POST.get('num'))
        # print(type(id),id,type(num),num)
        # print(request.session['goods'])
        # 查看是否登录，登录购物车加数据库，没登录session
        try:
            # 直接获取session 登录id， 如果获取不到，报错执行except，获取的到，代表登陆，执行try
            user = request.session['user_id']
            ShoppingCart.objects.filter(goods_id=id,user_id=user).update(nums=num)
            return JsonResponse({'code': 200})
        except:
            # 没登陆
            goods = request.session.get('goods')
            # print(goods)
            goods[id]=num
            # print(goods)
            request.session['goods'] = goods
            return  JsonResponse({'code': 200})

def place_order(request):
    if request.method == 'GET':
        user_address = UserAddress.objects.all()
        user = request.session['user_id']
        goods = ShoppingCart.objects.filter(user_id=user).all()
        return render(request, 'place_order.html',{'add':user_address,'goods':goods})