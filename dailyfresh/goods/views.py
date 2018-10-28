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
from django.core.cache import cache
from redis import StrictRedis
from django.core.paginator import Paginator
from cart.views import get_cart_count
# Create your views here.
class Index(LoginRequiredMixin,View):
    def get(self,request):
        context=cache.get('cache_index')
        if context==None:
            print('设置缓存')
            goodstype_list = GoodsType.objects.all()
            IndexGoodsBanner_list = IndexGoodsBanner.objects.all().order_by('index')
            IndexPromotionBanner_list=IndexPromotionBanner.objects.all().order_by('index')


            for i in goodstype_list:
                image_set=IndexTypeGoodsBanner.objects.filter(type=i,display_type=1).order_by('index')
                bittle_set=IndexTypeGoodsBanner.objects.filter(type=i,display_type=0).order_by('index')

                i.image_banners=image_set
                i.bittle_banners=bittle_set
            # 准备数据字典
            context = {
                'goodstype_list': goodstype_list,
                'IndexGoodsBanner_list':IndexGoodsBanner_list,
                'IndexPromotionBanner_list':IndexPromotionBanner_list,
            }
            cache.set('cache_index',context,3600)
        cart_count = get_cart_count(request.user)
        context.update(cart_count=cart_count)
        # 返回渲染
        return render(request, 'dailyfresh/index.html', context)



class Detail(LoginRequiredMixin,View):
    '''详情页'''
    def get(self,request,skuid):
        '''显示详情页'''
        goods=GoodsSKU.objects.get(id=skuid)
        #获取商品的分类信息
        types=GoodsType.objects.all()
        #获取新品信息
        new_skus=GoodsSKU.objects.filter(type=goods.type).order_by('-create_time')[:2]

        #获取同一个spu的其他规格商品,后期扩展
        same_spu_skus=GoodsSKU.objects.filter(goods=goods.goods).exclude(id=goods.id)
        user=request.user
        if user.is_authenticated():
            #添加用户的历史记录
            #连接redis
            conn=StrictRedis('192.168.12.166')
            #key
            history_key='history_%d'%user.id
            #一处列表中的goods_id
            conn.lrem(history_key,0,goods.id)
            #把goods.id插入到列表的左侧
            conn.lpush(history_key,goods.id)
            #只保存用户最新浏览的5条信息
            conn.ltrim(history_key,0,4)
        #获取用户购物车中的商品的数目
        cart_count = get_cart_count(request.user)
        content={
            'types':types,
            'goods':goods,
            'new_skus':new_skus,
            'cart_count':cart_count,
            'same_spu_skus':same_spu_skus
        }
        return render(request,'dailyfresh/detail.html',content)

class List(LoginRequiredMixin,View):
    def get(self,request,type_id,page):
        '''显示列表页'''
        #获取种类信息
        try:
            type=GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse('goods:index'))
        #获取商品的分类信息
        types=GoodsType.objects.all()
        #获取排序方式 #获取分类商品的信息
        #sort=default 按照默认id排序
        #sort=price 按照商品价格排序
        #sort=hot 按照商品销量排序
        sort=request.GET.get('sort')
        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort=='hot':
            skus=GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort='default'
            skus=GoodsSKU.objects.filter(type=type).order_by('-id')
        #对数据进行分页
        paginator=Paginator(skus,1)
        #获取第page页内容
        try:
            page=int(page)
        except Exception as e:
            page=1
        if page>paginator.num_pages:
            page=1
        #获取第page页的Page实例对象
        skus_page=paginator.page(page)
        #todo:进行页码的控制,页面上最多显示五个页码
        num_pages=paginator.num_pages
        if num_pages<5:
            pages=range(1,num_pages+1)
        elif page<=3:
            pages=range(1,6)
        elif num_pages-page<=2:
            pages=range(num_pages-4,num_pages+1)
        else:
            pages=range(page-2,page+3)
        #获取新品信息
        new_skus=GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]
        #获取用户购物车商品的数目

        cart_count=get_cart_count(request.user)
        #组织模板上下文
        context={
            'type':type,'types':types,
            'skus_page':skus_page,
            'new_skus':new_skus,
            'cart_count':cart_count,
            'pages':pages,
            'sort':sort
        }
        #使用模板
        return render(request,'dailyfresh/list.html',context)
def query(request):
    return render(request,'search/query.html')