from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import User
from django.views.generic import View
import re


# Create your views here.
class Register(View):
    def get(self, request):
        return render(request, 'dailyfresh/register.html')

    def post(self, request):
        user_name = request.POST.get("user_name", '').strip().lower()
        user_pwd = request.POST.get("pwd", '').strip().lower()
        user_email = request.POST.get('email', '').strip().lower()
        user_allow = request.POST.get('allow')
        # 验证数据完整性
        if not all([user_name, user_pwd, user_email, user_allow]):
            return render(request, 'dailyfresh/register.html', {'errors': '数据不完整'})
        # 验证邮箱
        if not re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', user_email):
            return render(request, 'dailyfresh/register.html', {'errors': '邮箱地址不正确'})
        if user_allow != 'on':
            return render(request, 'dailyfresh/register.html', {'errors': '请同意用户协议'})

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'dailyfresh/register.html', {'errors': '用户名已存在'})
        user = User.objects.create_user(user_name, user_email, user_pwd, )
        user.is_active = 0
        user.save()
        print(user_name)
        return render(request, 'dailyfresh/login.html')


class Login(View):
    def get(self, request):
        return render(request, 'dailyfresh/login.html')


class Register_verify(View):
    def get(self, request):
        print(1)
        user_name = request.GET.get('user_name')
        print(user_name)
        if 5 < len(user_name) < 20:
            return HttpResponse('用户名可用')
        else:
            return HttpResponse('用户名非法')
