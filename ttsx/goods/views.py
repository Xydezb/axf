from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


from goods.models import Goods, liulan

from utils.functions import session_login



# @session_login
def goodlist(request):
    if request.method == 'GET':
        # 推荐的商品
        new_user = Goods.objects.all().order_by('-id')[:3]
        #商品分页
        page = int(request.GET.get('page', 1))
        users = Goods.objects.all()
        p = Paginator(users, 15)
        users = p.page(page)
        return render(request, 'list.html', {'users': users, 'new_user': new_user})



def detail(request):
    if request.method == 'GET':
        #取到每个商品id
        id = int(request.GET.get('id'))
        #与商品表过滤得到变量users1
        users1 = Goods.objects.filter(id=id).first()

       #这里是判断浏览表里有没有此商品id
        LL = liulan.objects.filter(goodsid_id=id)
        #如果浏览表里没有此商品id 就往下添加
        if not LL:
            # 浏览表添加商品id，与商品表成外键关系
            liulan.objects.create(goodsid_id=id)

        #这里只要5条商品信息，其余删除     遍历表长度减5，默认从开头遍历
        for i in range(len(liulan.objects.all())-5):
            #每次拿到第一个就删掉
            liulan.objects.first().delete()
        # print(len(liulan.objects.all()))
        return render(request, 'detail.html', {'users': users1})
