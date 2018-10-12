import hashlib
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse


#md5加密
def my_md5(value):
    m = hashlib.md5()
    m.update(value.encode("utf-8"))
    return m.hexdigest()


#登录用的装饰器
def my_login(func):
    def innner(*args,**kwargs):
        login_user_id = args[0].session.get("login_user_id")
        if login_user_id:
            return func(*args,**kwargs)
        else:
            resp = redirect(reverse("user:login"))
            #记录之前的url
            resp.set_cookie("url_dest",args[0].get_full_path())

            return resp
    return innner




# @my_login  相当于  select_by_id = my_login(select_by_id)

# def select_by_id(request,bid):
#     bookinfo = BookInfo.objects.get(id=bid)
#     return render(request, "book/book_detail.html", {"bookinfo": bookinfo})