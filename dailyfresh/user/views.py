# encoding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import User
from django.views.generic import View
from PIL import Image, ImageDraw, ImageFont
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as tjwss, SignatureExpired,BadSignature
import random
from io import BytesIO
import re
from dailyfresh import settings
from django.core.mail import send_mail


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
        '''发送激活邮件，也包含激活链接：http://ip:port/user/active/3
            激活链接中需要包含用户的身份信息，并且要把身份信息进行加密
        '''
        # 加密用户的身份信息，生成激活ｔｏｋｅｎ
        print(1)
        serializers = tjwss(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializers.dumps(info).decode()

        encryption_url = "http://192.168.12.166:8888/user/active/%s" % token
        print(2)

        # 发邮件
        subject = '天天生鲜欢迎信息'  # 邮件主题
        message = ''  # 文本内容
        sender = settings.EMAIL_FROM  # 发件人
        print(user_email)
        receiver = [user_email]  # 收件人
        print(receiver)
        html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="%s">%s</a>' % (
        user_name, encryption_url, encryption_url)
        print(3)
        send_mail(subject, message, sender, receiver, html_message=html_message)
        print(4)
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


def validate_code(request):
    # 定义变量，用于画面的背景色、宽、高
    # bgcolor = (random.randrange(256), random.randrange(256), random.randrange(256))
    bgcolor = (255, 255, 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 200):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'abcd123efgh456ijklmn789opqr0stuvwxyzABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 保存到sesison
    request.session["validate_code"] = rand_str

    # 构造字体对象
    font = ImageFont.truetype(settings.FONT_STYLE, 23)
    # 绘制4个字
    for i in range(4):
        # 构造字体颜色
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((5 + 23 * i, 2), rand_str[i], font=font, fill=fontcolor)

    # 释放画笔
    del draw
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def email(request):
    email = '27409517@qq.com'
    subject = '11'
    message = '11'
    sender = settings.EMAIL_FROM
    receiver = [email]
    send_mail(subject, message, sender, receiver)
    return HttpResponse('ok')
class ActiveView(View):
    def get(self,request,token):
        serializers=tjwss(settings.SECRET_KEY,3600)
        try:
            info=serializers.loads(token)
            user_id=info['confirm']
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            return  redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')
        except BadSignature as e:
            return HttpResponse('激活链接非法')