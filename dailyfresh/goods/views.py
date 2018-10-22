from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import User
from django.http  import response
from django.views.generic import View
from PIL import Image, ImageDraw, ImageFont
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as tjwss, SignatureExpired,BadSignature
import random
import re
from dailyfresh import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from celery_tasks.tasks import send_register_active_email
from util.user_util import LoginRequiredMixin
from  goods.models import *
# Create your views here.
class Index(LoginRequiredMixin,View):
    def get(self,request):
        goodstype_list = GoodsType.objects.all()
        IndexGoodsBanner_list = IndexGoodsBanner.objects.all().order_by('index')
        IndexPromotionBanner_list=IndexPromotionBanner.objects.all().order_by('index')


        for i in goodstype_list:
            image_set=IndexTypeGoodsBanner.objects.filter(type=i,display_type=1).order_by('index')
            bittle_set=IndexTypeGoodsBanner.objects.filter(type=i,display_type=0).order_by('index')

            i.image_banners=image_set
            i.bittle_banners=bittle_set

        cart_count=0

            # for i in IndexTypeGoodsBanner_list:
            #     if i.display_type==0:
            #         image_list.append(i)
            #     elif i.display_type==1:
            #         bittle_list.append(i)

        # 准备数据字典
        context = {
            'goodstype_list': goodstype_list,
            'IndexGoodsBanner_list':IndexGoodsBanner_list,
            'IndexPromotionBanner_list':IndexPromotionBanner_list,
            'cart_count':cart_count
        }
        # 返回渲染
        return render(request, 'dailyfresh/index.html', context)
class Test(LoginRequiredMixin,View):
    def get(self,request):
        #获取商品信息种类
        goodstype_list=GoodsType.objects.all()
        #准备数据字典
        context={'goodstyle_list':goodstype_list}
        #返回渲染
        return render(request,'dailyfresh/test1.html',context)