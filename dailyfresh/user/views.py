# encoding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import User,Address
from django.http  import response
from django.views.generic import View
from PIL import Image, ImageDraw, ImageFont
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as tjwss, SignatureExpired,BadSignature
import random
from io import BytesIO
import re
from dailyfresh import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from celery_tasks import tasks
from util.user_util import LoginRequiredMixin
from redis import StrictRedis
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods
from django.core.paginator import Paginator
# Create your views here.
class Register(View):
    def get(self, request):
        return render(request, 'dailyfresh/register.html')
    @csrf_exempt
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


        # 发邮件
        subject = '天天生鲜欢迎信息'  # 邮件主题
        message = ''  # 文本内容
        sender = settings.EMAIL_FROM  # 发件人
        print(user_email)
        receiver = [user_email]  # 收件人
        print(receiver)
        html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="%s">%s</a>' % (
        user_name, encryption_url, encryption_url)

        tasks.send_register_active_email.delay(subject, message, sender, receiver, html_message)
        return render(request, 'dailyfresh/login.html')


class Login(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
            checked='checked'
        else:
            username=''
            checked=''
        return  render(request, 'dailyfresh/login.html', {'username':username, 'checked':checked})
    def post(self,request):
        username=request.POST.get('username')
        userpwd=request.POST.get('pwd')
        # 获取属性
        validate = request.POST.get("validate_code_input", "").strip().lower()
        print(validate)
        if validate != request.session.get("validate_code").lower():
            return redirect(reverse("user:login"))
        if not all([username,userpwd]):
            return render(request, 'dailyfresh/login.html', {'error': '用户数据不完整'})
        user = authenticate(username=username, password=userpwd)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request,user)
                next_url=request.GET.get('next')
                if next_url:
                   return redirect(next_url)
                else:
                    response=redirect(reverse('goods:index'))
                remember=request.POST.get('remember')
                if remember=='on':
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                return render(request, 'dailyfresh/login.html', {'error': '用户名未激活'})
        else:
            # the authentication system was unable to verify the username and password
            return render(request, 'dailyfresh/login.html', {'error': '用户名或密码有误'})



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
    bgcolor = (255,255,255)
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


    #保存到sesison
    request.session["validate_code"] = rand_str

    # 构造字体对象
    font = ImageFont.truetype(settings.FONT_STYLE, 23)
    # 绘制4个字
    for i in range(4):
        # 构造字体颜色
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((5+23*i, 2), rand_str[i], font=font, fill=fontcolor)

    # 释放画笔
    del draw

    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def email(request):
    email = '1430453115@qq.com'
    subject = '您有一张自拍已上传,点击查看'
    message=''
    a='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540211224&di=935842e0cfb4b31588aa7a96ecb50d00&imgtype=jpg&er=1&src=http%3A%2F%2Fimg1.sc115.com%2Fuploads%2Fsc%2Fjpg%2F144%2F18892.jpg'
    html_message= '<h1>尊敬的王女士,您好/h1><br><a href="%s">点击链接,查看照片</a>'%a
    sender = settings.EMAIL_FROM
    receiver = [email]

    send_mail(subject, message, sender, receiver,html_message=html_message)
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
class Update_password(View):
    def get(self,request):
        return render(request,'dailyfresh/update_password.html')
    def post(self,request):
        username=request.POST.get('username').strip().lower()
        useremail=request.POST.get('useremail').strip().lower()

        if not all([username,useremail]):
            return render(request,'dailyfresh/update_password.html',{'error':'数据不完整'})
        if not re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', useremail):
            return render(request, 'dailyfresh/update_password.html', {'errors': '邮箱地址不正确'})
        if not User.objects.get(username=username):
            return render(request,'dailyfresh/update_password.html',{'errors':'用户名不存在'})
        '''发送激活邮件，也包含激活链接：http://ip:port/user/active/3
                   激活链接中需要包含用户的身份信息，并且要把身份信息进行加密
               '''
        user=User.objects.get(username=username)
        # 加密用户的身份信息，生成激活ｔｏｋｅｎ
        serializers = tjwss(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializers.dumps(info).decode()

        encryption_url = "http://192.168.12.166:8888/user/update_password1/%s" % token

        # 发邮件
        subject = '天天生鲜欢迎信息'  # 邮件主题
        message = ''  # 文本内容
        sender = settings.EMAIL_FROM  # 发件人

        receiver = [useremail]  # 收件人

        html_message = '<h1>%s,欢迎您</h1>请点击以下链接修改您的密码<br><a href="%s">%s</a>' % (
            username, encryption_url, encryption_url)

        tasks.send_update_password_email.delay(subject, message, sender, receiver, html_message)
        return redirect('user:login')
class Update_password1(View):
    def get(self,request,token):
        return render(request,'dailyfresh/update_new_password.html',{'token':token})
class Update_password2(View):
    def post(self,request):
        token=request.POST.get('token')
        print(0,token)
        serializers=tjwss(settings.SECRET_KEY,3600)
        try:
            info=serializers.loads(token)
            user_id=info['confirm']
            print(1,user_id)
            userpwd=request.POST.get('userpwd')
            print(2,userpwd)
            user=User.objects.get(id=user_id)
            user.set_password(userpwd)
            user.save()
            return  redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')
        except BadSignature as e:
            return HttpResponse('激活链接非法')
class User_center_info(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        try:
            address = Address.objects.filter(user=user)
        except Address.DoesNotExist:
            address = None

        #读取历史记录
        #连接redis
        conn=StrictRedis('192.168.12.166')
        history=conn.lrange('history_%d'%user.id ,0,-1)
        # goodsskus=GoodsSKU.objects.filter(id__in=history)
        goodsskus=[]
        for i in history:
            j=GoodsSKU.objects.get(id=i)
            goodsskus.append(j)
        context = {'page': '1', 'address': address,'goodsskus':goodsskus}
        return render(request, 'dailyfresh/user_center_info.html', context)

class User_center_order(LoginRequiredMixin,View):
    def get(self, request,page):
        '''显示'''
        #获取用户的订单信息
        user=request.user
        orders=OrderInfo.objects.filter(user=user).order_by('-create_time')
        #遍历获取订单商品的信息
        for order in orders:
            order_skus=OrderGoods.objects.filter(order_id=order.order_id)

            #遍历order_skus计算商品的小计
            for order_sku in order_skus:
                #计算小计
                amount=order_sku.count*order_sku.price
                #动态的给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount=amount
            ###动态的给order增加属性,保存订单商品状态标题
            order.status_name=OrderInfo.ORDER_STATUS[order.order_status]
            ##动态的给order增加属性,保存订单商品的信息
            order.order_skus=order_skus
        #分页
        paginator=Paginator(orders,1)
        # 获取第page页内容
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        # 获取第page页的Page实例对象
        order_page = paginator.page(page)
        # todo:进行页码的控制,页面上最多显示五个页码
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)
        #组织上下文
        context = {'page': '2','order_page':order_page,'pages':pages,}
        return render(request, 'dailyfresh/user_center_order.html',context)
class User_center_site1(LoginRequiredMixin,View):
    def get(self, request):
        user=request.user
        address_id = request.GET.get('address_id')
        print(address_id)
        try:
            address=Address.objects.get(user=user,id=address_id)
        except Address.DoesNotExist:
            address=None
        context = {'page': '3','address':address}
        return render(request, 'dailyfresh/user_center_site1.html',context)
    def post(self,request):
        #获取传输值
        address_id=request.GET.get('address_id')
        province=request.POST.get('province')
        town=request.POST.get('town')
        receiver=request.POST.get('receiver')
        addr=request.POST.get('addr')
        addr=province+town+addr
        zip_code=request.POST.get('zip_code')
        phone=request.POST.get('phone')
        is_default=request.POST.get('is_default')
        #数据校验
        if not all([receiver,addr,zip_code,phone]):
            return render(request,'dailyfresh/user_center_site.html',{'error':'数据不完整'})
        if not re.match('^((13[0-9])|(14[5,7,9])|(15[^4])|(18[0-9])|(17[0,1,3,5,6,7,8]))\d{8}$',phone):
            return render(request, 'dailyfresh/user_center_site.html', {'error': '手机号码不正确'})
        #数据处理
        user=request.user
        try:
            address=Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            address=None
        if address:
            is_default=False
        else:
            is_default=True
        if address_id:
            address=Address.objects.get(id=address_id)
            address.receiver=receiver
            address.addr=addr
            address.zip_code=zip_code
            address.phone=phone
            address.save()
            return redirect(reverse('user:user_center_site'))
        else:
            #添加地址
            Address.objects.create(user=user,receiver=receiver,addr=addr,zip_code=zip_code,phone=phone,is_default=is_default)
            #返回应答,刷新页面
            return redirect(reverse('user:user_center_site'))
class User_center_site(LoginRequiredMixin,View):
    def get(self, request):
        user=request.user
        try:
            address=Address.objects.filter(user=user)
        except Address.DoesNotExist:
            address=None
        context = {'page': '3','address':address}
        return render(request, 'dailyfresh/user_center_site.html',context)
    def post(self,request):
        #获取传输值
        province=request.POST.get('province')
        town=request.POST.get('town')
        receiver=request.POST.get('receiver')
        addr=request.POST.get('addr')
        addr=province+town+addr
        zip_code=request.POST.get('zip_code')
        phone=request.POST.get('phone')
        is_default=request.POST.get('is_default')
        #数据校验
        if not all([receiver,addr,zip_code,phone]):
            return render(request,'dailyfresh/user_center_site.html',{'error':'数据不完整'})
        if not re.match('^((13[0-9])|(14[5,7,9])|(15[^4])|(18[0-9])|(17[0,1,3,5,6,7,8]))\d{8}$',phone):
            return render(request, 'dailyfresh/user_center_site.html', {'error': '手机号码不正确'})
        #数据处理
        user=request.user
        try:
            address=Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            address=None
        if address:
            is_default=False
        else:
            is_default=True
        #添加地址
        Address.objects.create(user=user,receiver=receiver,addr=addr,zip_code=zip_code,phone=phone,is_default=is_default)
        #返回应答,刷新页面
        return redirect(reverse('user:user_center_site'))
class User_center_site_handler(LoginRequiredMixin,View):
    def get(self,request,):
        a=request.GET.get('a')
        address_id=request.GET.get('address_id')
        if a=='1':
            address=Address.objects.get(id=address_id)
            address.delete()
            return redirect(reverse('user:user_center_site'))
        elif a=='2':
            address = Address.objects.get(id=address_id)
            user=request.user
            print(user)
            for i in Address.objects.filter(user=user):
                i.is_default=False
                i.save()
            address.is_default = True
            address.save()
            return redirect(reverse('user:user_center_site'))

class Loginout(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return render(request,'dailyfresh/login.html')
