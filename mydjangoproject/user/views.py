from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from user.models import *
from utils.user_util import my_md5
from book import views as book_views
from django.core.urlresolvers import reverse
from utils import user_util
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from django.conf import settings
from book.models import *
# from mydjangoproject import settings
import urllib


def select_all_area(request):
    area_list = Area.objects.filter(parent__isnull=True)
    return render(request, "user/area_list.html", {"area_list": area_list, "title": "显示所有的area"})


def select_area_by_id(request, area_id):
    area_list = Area.objects.filter(parent_id=area_id)
    return render(request, "user/area_list.html", {"area_list": area_list, "title": "显示所有的area"})


def register(request):
    return render(request, "user/register.html")


def register_handler(request):
    # 判断请求方式
    if request.method == "GET":
        request_info = request.GET
    else:
        request_info = request.POST

    # 获取属性
    user_name = request_info.get("user_name","").strip()
    user_pwd = request_info.get("user_pwd","").strip()

    # 判断
    errors = {}
    if user_name == "":
        errors["user_name"] = "用户名必填"
    elif not 6<=len(user_name)<=10:
        errors["user_name"] = "用户名长度必须是6-10位"
    elif User.objects.filter(name=user_name):
        errors["user_name"] = "用户名已存在"


    if user_pwd.strip() == "":
        errors["user_pwd"] = "密码必填"


    if errors:
        return render(request, "user/register.html", {"errors": errors,"user_name":user_name,"user_pwd":user_pwd})
    else:
        # 新增
        user = User.objects.create(name=user_name, pwd=my_md5(user_pwd))
        return HttpResponseRedirect(reverse("user:login"))


def login(request):

    #获取cookie
    remember_user_name = request.COOKIES.get("remember_user_name","")
    return render(request, "user/login.html",{"remember_user_name":remember_user_name})


def login_handler(request):
    """
    cookie-验证
    1、验证用户名
    2、密码
    3、验证码
    """


    # 获取属性
    validate = request.POST.get("validate_code","").strip().lower()

    # resp = HttpResponseRedirect(reverse("user:login"))
    # if validate=="":
    #     resp.set_cookie("error_validate_code","验证码必填")
    #     return resp
    # elif validate!=request.session.get("validate_code").lower():
    #     resp.set_cookie("error_validate_code", "验证码错误")
    #     return resp
    # else:

    if validate!=request.session.get("validate_code").lower():
        return HttpResponseRedirect(reverse("user:login"))

    user_name = request.POST.get("user_name","").strip()
    user_pwd = request.POST.get("user_pwd","").strip()
    remember = request.POST.get("remember")
    user_pwd = my_md5(user_pwd)

    # 查询
    user = User.objects.filter(name=user_name, pwd=user_pwd)
    if len(user) != 0:
        #将登录信息保存到session
        request.session["login_user_id"] = user[0].id

        #判断是否跳转到上一次的页面
        url_dest = request.COOKIES.get("url_dest")
        if url_dest:
            resp = HttpResponseRedirect(url_dest)
            resp.delete_cookie("url_dest")
        else:
            #删除验证码
            del request.session["validate_code"]

            resp = HttpResponseRedirect(reverse("book:index"))

        #记住用户名
        if remember=="1":
            resp.set_cookie("remember_user_name",user_name,3600*24*7)
        else:
            resp.set_cookie("remember_user_name", user_name, 0)
        return resp
    else:
        return HttpResponseRedirect(reverse("user:login"))


def logout(request):
    #清除session
    request.session.flush()
    return redirect(reverse("book:index"))

@user_util.my_login
def modify_pwd(request):
    return render(request, "user/modify_pwd.html")


@user_util.my_login
def modify_pwd_handler(request):
    #获取参数
    new_pwd = request.POST.get("new_pwd").strip()
    #获取session中的用户
    login_user_id = request.session["login_user_id"]
    user = User.objects.get(id=login_user_id)
    #修改
    user.pwd = my_md5(new_pwd)
    user.save()

    return HttpResponse("修成成功，当前新的密码是：%s"%new_pwd)


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

def set_cookie(request):
    resp = HttpResponse("set_cookie")
    resp.set_cookie("num",100,3600*24)
    resp.set_cookie("name",urllib.parse.quote("老王"),3600*24)
    resp.set_cookie("cookie1","laowang",0)
    resp.set_cookie("cookie2","laowang2",-1)

    return resp


def get_cookie(request):
    print(request.COOKIES)
    print(urllib.parse.unquote(request.COOKIES.get("name")))

    return HttpResponse("get_cookie")



def set_session(request):
    request.session.set_expiry(3600*24*14)
    request.session["session1"] = "value1"
    request.session["session2"] = "value2"
    request.session["session2"] = "老王"

    return HttpResponse("set_session")


def get_session(request):
    print(request.session.get("session1"))
    print(request.session.get("session2"))

    return HttpResponse("get_session")


def del_session(request):
    #删除所有与本地浏览器相关的sesison
    # request.session.flush()
    #删除某一个与本地浏览器相关的sesison
    del request.session["session1"]

    return HttpResponse("del_session")



def func():
    return "xx"

def variable(request):
    cxt={
        "k1":"老王",
        "k2":User.objects.get(id=1),
        "k3":{"a":10,"b":20,"c":func},
        "k4":[110,120,119],
        "k5":User.objects.all(),
        "k6":False,
        "title":"韩国bf风加厚保暖面包服中长款宽松棒球外套丝绒羽绒服女XX"
    }
    return render(request,"test/test01.html",cxt)
def user_name_handler(request):
    user_name=request.GET.get('user_name').strip()
    print(user_name)
    if not user_name:
        return HttpResponse('用户名不能为空')
    else:
        if User.objects.filter(name=user_name):
             return HttpResponse('用户名已存在')
        else:
            return HttpResponse('用户名可用')