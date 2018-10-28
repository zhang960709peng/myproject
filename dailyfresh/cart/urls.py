"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from cart.views import *


urlpatterns = [
    url(r'^add$', CartAddView.as_view(), name='add'),#购物车记录添加
    url(r'^$', CartInfoView.as_view(), name='show'),#购物车页面显示
    url(r'^update$', CartUpdateView.as_view(), name='update'),#购物车记录 更新
    url(r'^delete$', CartDetleView.as_view(), name='delete'),#购物车记录删除
    url(r'^count$', CartCountView.as_view(), name='count'),#获取购物车数量

]