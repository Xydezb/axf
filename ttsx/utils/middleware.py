import re

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import User


class UserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        # print(user_id)
        if user_id:
            user = User.objects.get(id = user_id)
            print(user)
            request.user = user.username
        # print(user)
        else:
            request.user = user_id            #往前端返回一个对象，用来渲染

        #中间件登录校验
        #过滤不需要做登录校验的地址
        path = request.path
        print(request.path,request.user)
        not_neet_login = ['/user/index','/user/login','/user/register','/user/logout', '/goods/goodlist','/goods/detail', '/carts/index','/carts/add_cart','/carts/change_cart',
                          '/media/(.*)']
        for not_neet_path in not_neet_login:
            if re.match(not_neet_path, path):
                return None

        # if re.match ['/user/login/', '/user/register/', '/user/index/', '/carts/index/', '/goods/index/', '/goods/goodlist/','/goods/detail/', '/media/(.*)']:
        #     return None

        #登录校验
        # user_id = request.session.get('user_id')
        print('****************')
        if not user_id:
            # return HttpResponseRedirect(reverse('user:register'))
            return redirect('user:login')  #重定向和上面那个一样作用
        else:
            return redirect('user:index')

        # return None
