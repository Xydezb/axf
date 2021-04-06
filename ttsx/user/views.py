from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from goods.models import liulan, GoodsCategory, Goods
from user.form import UserForm, LoginForm
from user.models import User
# from utils.functions import session_login


# @session_login
def index(request):
    # 商品分类标题
    gdlist = GoodsCategory.objects.all()
    # print(gdlist)

    #各类商品前4条信息
    list1 = Goods.objects.filter(category_id=1)[0:4]
    list2 = Goods.objects.filter(category_id=2)[0:4]
    list3 = Goods.objects.filter(category_id=3)[0:4]
    list4 = Goods.objects.filter(category_id=4)[0:4]
    list5 = Goods.objects.filter(category_id=5)[0:4]
    list6 = Goods.objects.filter(category_id=6)[0:4]

    # 各类商品点击量前三条
    goods_type01 = Goods.objects.filter(category_id=1).order_by('-click_nums')[0:4]
    goods_type02 = Goods.objects.filter(category_id=2).order_by('-click_nums')[0:4]
    goods_type03 = Goods.objects.filter(category_id=3).order_by('-click_nums')[0:4]
    goods_type04 = Goods.objects.filter(category_id=4).order_by('-click_nums')[0:4]
    goods_type05 = Goods.objects.filter(category_id=5).order_by('-click_nums')[0:4]
    goods_type06 = Goods.objects.filter(category_id=6).order_by('-click_nums')[0:4]

    # 拼接，合并成字典，传到前端渲染
    goods_type = {
        'goods_type1': [goods_type01, goods_type01, gdlist[0]],
        'goods_type2': [goods_type02, goods_type02, gdlist[1]],
        'goods_type3': [goods_type03, goods_type03, gdlist[2]],
        'goods_type4': [goods_type04, goods_type04, gdlist[3]],
        'goods_type5': [goods_type05, goods_type05, gdlist[4]],
        'goods_type6': [goods_type06, goods_type06, gdlist[5]],
    }
    # print()
    return render(request, 'index.html',{'goodstype': goods_type })

#登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 到这里字段表单里字段正确，且数据库里有此用户名
            username = form.cleaned_data['username']

            password = form.cleaned_data['password']
            user = User.objects.get(username=username)

            #校验密码是否一致
            if not check_password(password, user.password):
                pwd_error = '密码错误'
                return render(request, 'login.html', {'pwd_error': pwd_error})
            #密码通过
            res = HttpResponseRedirect(reverse('user:index'))
            #设置缓存，session
            request.session['user_id'] = user.id
            return res

        errors = form.errors
        return render(request,'login.html', {'errors': errors})


#注册
def register1(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        #表单校验
        form = UserForm(request.POST)
        if form.is_valid():
            #表单校验成功
            username = form.cleaned_data.get('username')
            password = make_password(form.cleaned_data.get('pwd1'))
            email = form.cleaned_data.get('email')
            User.objects.create(username=username,password=password,email=email)

            #重定向登录页面
            return HttpResponseRedirect(reverse('user:login'))

    errors = form.errors
    return render(request, 'register.html',{'errors':errors})

#用户中心
# @session_login
def UserCenter(request):
    if request.method == 'GET':
        gs = liulan.objects.all()
        return render(request, 'user_center_info.html',{'gs':gs})

#注销
def logout(request):
    if request.method == 'GET':
        request.session.flush()
        # return HttpResponseRedirect(reverse('user:login'))
        return redirect(reverse('user:login'))


