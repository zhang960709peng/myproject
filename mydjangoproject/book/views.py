from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader, RequestContext
from book.models import *
from django.core.urlresolvers import reverse
from utils import user_util
from user.models import *
from django.conf import settings
from utils.book_util import *
from django.core.paginator import Paginator
import os
import json
from django.core.serializers import serialize

"""
def index(request):
    #获取版本对象
    my_template = loader.get_template("book/index.html")
    #上下文对象
    cxt = RequestContext(request,{"name":"老王"})
    #响应内容
    content = my_template.render(cxt)
    #响应对象
    resp = HttpResponse(content)
    #返回
    return resp
"""


def index(request):
    return render(request, "book/index.html")


@user_util.my_login
def book_select_all(request):

    book_list = BookInfo.objects.all()

    login_user_id = request.session["login_user_id"]
    if login_user_id:
        user = User.objects.filter(id=login_user_id)[0]

    cxt = {
        "book_list": book_list,
        "user_name":user.name,
        "title":"查询所有的bookinfo"
    }
    return render(request, "book/book_list.html", cxt)


@user_util.my_login
def book_select_by_id(request, bid):
    bookinfo = BookInfo.objects.get(id=bid)
    return render(request, "book/book_detail.html", {"bookinfo": bookinfo})



@user_util.my_login
def hero_select_all(request):
    return render(request,'book/heroinfo_list_page.html')



@user_util.my_login
def hero_select_all2(request):
    login_user_id = request.session["login_user_id"]
    if login_user_id:
        user = User.objects.filter(id=login_user_id)[0]

    heroinfo_list = HeroInfo.objects.all()
    return render(request, "book/heroinfo_list.html", {"heroinfo_list": heroinfo_list,"user_name":user.name,"title":"查询所有的heroinfo"})




@user_util.my_login
def hero_select_by_id(request, hid):
    heroinfo = HeroInfo.objects.get(id=hid)
    return render(request, "book/heroinfo_detail.html", {"heroinfo": heroinfo})



# .../heroinfo/edit?hid=10
@user_util.my_login
def hero_edit(request):

    #准备数据1：要修改的heroinfo
    hid = request.GET.get("hid")
    heroinfo = HeroInfo.objects.get(id=hid)

    # 准备数据2：所有的bookinfo
    book_list = BookInfo.objects.all()

    return render(request, "book/heroinfo_edit_insert.html", {"heroinfo": heroinfo,"book_list":book_list})
    # return render(request, "book/heroinfo_edit.html", {"heroinfo": heroinfo,"book_list":book_list})





@user_util.my_login
def hero_edit_handler(request):

    #接受参数

    hid = request.POST.get("hid")
    hname = request.POST.get("hname")
    hgender = request.POST.get("hgender")
    hcontent = request.POST.get("hcontent")
    hbookinfo_id = request.POST.get("hbookinfo_id")
    isdelete = request.POST.get("isdelete",False)
    hpic = request.FILES["hpic"]

    # 查询
    heroinfo = HeroInfo.objects.get(id=hid)


    """删除原来的图片"""
    os.remove(os.path.join(settings.MEDIA_ROOT, heroinfo.hpic.name))

    """保存到本地"""
    hpic_chunks = hpic.chunks()
    file_name = os.path.join("images", do_file_name(hpic.name))
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(file_path, "wb") as file:
        for chunk in hpic_chunks:
            file.write(chunk)
    """更新数据库"""
    #见修改





    #修改
    heroinfo.hname = hname
    heroinfo.hgender = True if hgender=="1" else False
    heroinfo.hcontent = hcontent
    heroinfo.hbookinfo_id = hbookinfo_id
    heroinfo.isdelete = isdelete
    heroinfo.hpic = file_name
    heroinfo.save()

    return redirect(reverse("book:hero_select_by_id",args=[hid]))



@user_util.my_login
def hero_delete1(request):

    #接受参数
    hid = request.GET.get("hid")
    #查询
    heroinfo = HeroInfo.objects.get(id=hid)
    #删除
    heroinfo.delete()

    return redirect(reverse("book:hero_select_one_page",args=[1,]))


@user_util.my_login
def hero_delete2(request):

    #接受参数
    hid = request.GET.get("hid")
    #查询
    heroinfo = HeroInfo.objects.get(id=hid)
    #删除-更新
    if heroinfo.isdelete==False:
        heroinfo.isdelete = True

    heroinfo.save()

    return redirect(reverse("book:hero_select_all"))



@user_util.my_login
def hero_insert(request):

    # 准备数据：所有的bookinfo
    book_list = BookInfo.objects.all()

    return render(request, "book/heroinfo_edit_insert.html", {"book_list":book_list})
    # return render(request, "book/heroinfo_insert.html", {"book_list":book_list})



@user_util.my_login
def hero_insert_handler(request):

    #接受参数
    hname = request.POST.get("hname")
    hgender = request.POST.get("hgender")
    hcontent = request.POST.get("hcontent")
    hbookinfo_id = request.POST.get("hbookinfo_id")


    """上传的文件对应的对象"""
    hpic = request.FILES["hpic"]


    # print(hpic)
    # print(type(hpic))
    # print(dir(hpic))
    # print(hpic.name)
    #"<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>"
    #< class 'django.core.files.uploadedfile.TemporaryUploadedFile'>

    """文件保存到本地"""
    hpic_chunks = hpic.chunks()
    # print(type(hpic_chunks))

    #文件保存的路径
    file_name = os.path.join("images",do_file_name(hpic.name))
    file_path = os.path.join(settings.MEDIA_ROOT,file_name)

    #写
    with open(file_path,"wb") as file:
        for chunk in hpic_chunks:
            file.write(chunk)


    """文件的名字保存到数据库"""


    #新增
    heroinfo = HeroInfo()
    heroinfo.hname = hname
    heroinfo.hgender = True if hgender=="1" else False
    heroinfo.hcontent = hcontent
    heroinfo.hbookinfo_id = hbookinfo_id
    heroinfo.hpic = file_name
    heroinfo.save()

    return redirect(reverse("book:hero_select_all"))


def hero_page(request):
    import time,random
    time.sleep(random.random()*5)
    #获取页码
    pn=request.GET.get('pn')

    #分页对象
    my_paginator = Paginator(HeroInfo.objects.all().order_by("id"),5)
    #当前页对象
    my_page = my_paginator.page(pn)

    herinfo_list = my_page.object_list
    page_range=my_paginator.page_range
    page_now = pn
    if my_page.has_next():
        page_next=my_page.next_page_number()
        cxt = {
            "heroinfo_list": serialize('json', my_page.object_list, ensure_ascii=False),
            'page_range': page_range,
            'page_now': page_now,
            'page_next': page_next
        }
    else:
        cxt = {
            "heroinfo_list": serialize('json', my_page.object_list, ensure_ascii=False),
            'page_range': page_range,
            'page_now': page_now,

        }
    # b =my_page.next_page_number()
    # c =my_page.previous_page_number()
    # b=[]
    # for i in herinfo_list:
    #     c={}
    #     c['hname']=i.hname
    #     c['hid']=i.id
    #


    # json_str=json.dumps(cxt)

    return JsonResponse(cxt)
    # //返回字符串(内不是json格式)
    # '{'id':1,'name':'老王'}'
    #



def test(request):
    # import time
    # time.sleep(5)
    #
    # 1 / 0
    return HttpResponse("<h1>test...</h1>", content_type="text/plain; charset=utf-8")


def test1(request):
    num = 1/0  #模拟异常
    return render(request, "test/base.html")

def test2(request):
    return render(request, "test/main.html",{"my_title":"main"})

def test3(request):
    return render(request, "test/base_left_right.html")

def test4(request):
    return render(request, "test/user01.html",{"my_title":"user01"})


def test5(request):
    # return render(request, "test/test05.html",{"content":"<h1>1 > 0</h1>"})
    return render(request, "test/test05.html",{"content":"<script>alert('123')</script>"})

def test6(request):
    return render(request, "test/test06.html")

def test7(request):
    return render(request, "test/test07.html")

def test7_1(request):
    import time
    time.sleep(10)
    return HttpResponse("7_1")

def test7_2(request):
    return HttpResponse("7_2")

def test8(request):
    return render(request, "test/test08.html")

def test10(request):
    return render(request, "test/test10.html")

def test11(request):
    return render(request, "test/test11.html")

def test12(request):
    return render(request, "test/test12.html")
def heroinfo_search(request):
    return render(request, "book/heroinfo_search.html")
def heroinfo_search_handler(request):
    hname=request.GET.get('hname')
    if hname=='':
        dic={
            'ret':[]
        }
        return HttpResponse(json.dumps(dic, ensure_ascii=False), content_type="application/json;charset=utf-8")
    else:
        hero_list=HeroInfo.objects.filter(hname__contains=hname).values('hname','id')
        print(hero_list)
        ret=[]
        for i in hero_list:
            info = {}
            info['hname']=i['hname']
            info['hid']=i['id']
            ret.append(info)
        print(ret)
        dic={
            'ret':ret
        }


        return HttpResponse(json.dumps(dic,ensure_ascii=False),content_type="application/json;charset=utf-8")