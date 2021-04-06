from django.http import HttpResponseRedirect
from django.urls import reverse


def session_login(func):
    def check(request, *args, **kwargs):
        try:
            #从session中取数据，如果取得出user_id，表示登录
            request.session['user_id']
            return func(request, *args, **kwargs)
        except:
            return HttpResponseRedirect(reverse('user:register'))
    return check