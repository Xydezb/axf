from django import forms

from user.models import User

#用户
class UserForm(forms.Form):
    # required=True  这个字段必填，不能为空。
    username = forms.CharField(required=True,max_length=20,
                               error_messages={
                                   'required':'注册用户名必填',
                                   'max_length': '注册账号最长不超过20字符',
                               })
    pwd1 = forms.CharField(required=True,max_length=255,
                           error_messages={
                               'required':'注册密码必填',
                               'max_length': '注册密码最长不超过255字符',
                           })
    pwd2 = forms.CharField(required=True,max_length=255,
                           error_messages={
                               'required':'验证密码必填',
                               'max_length': '验证密码最长不超过255字符',
                           })
    email = forms.CharField(required=True,max_length=100,
                           error_messages={
                               'required':'邮箱必填',
                               'max_length': '验证密码最长不超过100字符',
                           })


    def clean(self):
        #用户名是否注册
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username':'用户名已存在，请切换'})

        pwd1 = self.cleaned_data.get('pwd1')
        pwd2 = self.cleaned_data.get('pwd2')
        if pwd1 != pwd2 :
            raise forms.ValidationError({'pwd1':'密码不一致'})
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20,
                               error_messages={
                                   'required': '登录用户名必填',
                                   'max_length': '登录账号最长不超过20字符',
                               })
    password = forms.CharField(required=True, max_length=10,
                               error_messages={
                                'required': '登录密码必填',
                                'max_length': '登录密码最长不超过10字符',
                                })

    def clean_username(self):
        #校验某个字段，返回校验字段的值
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('账号不存在')
        return self.cleaned_data.get('username')