from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from django.conf import settings
from util.user_util import LoginRequiredMixin


# Create your views here.
class CartAddView(View):
    '''购物车记录添加'''

    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        # 接受数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
            # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理:添加购物车记录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        # 先尝试获取水库_id的值_> hget cart_key 属性
        # 如果sku_id zai hash 中不存在,hget返None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            # 累加购物车中的商品的数目
            count += int(cart_count)
        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
        # 设置hash中sku_id对应的值
        conn.hset(cart_key, sku_id, count)
        total_count = conn.hlen(cart_key)
        # 计算用户购物车中商品的条目数
        # 返回应答
        return JsonResponse({'res': 5, 'total_count': total_count, 'errmsg': '添加成功'})


class CartInfoView(LoginRequiredMixin, View):
    '''购物车页面显示'''

    def get(self, request):
        '''显示'''
        # 获取登陆的用户
        user = request.user
        # 获取用户购物车中商品的信息
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        # {'商品id':商品的数量}
        cart_dict = conn.hgetall(cart_key)
        skus = []
        # 保存用户购物车中商品的总数目和总价格
        total_count = 0
        total_price = 0
        # 遍历商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id,获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给sku对象增加一个属性amount保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count保存购物车中对应商品的数量
            sku.count = count
            skus.append(sku)
            # 累加计算商品的总数目和总价格
            total_count += int(count)
            total_price += amount
        # 组织上下文
        context = {
            'total_count': total_count,
            'total_price': total_price,
            'skus': skus
        }
        return render(request, 'dailyfresh/cart.html', context)

class CartCountView(View):
    '''异步获取购物车总数量'''
    def get(self,request):
        total_count=get_cart_count(request.user)
        return JsonResponse({'total_count':total_count})
# 更新购物车记录
# 采用ajax post请求
# 前段需要传递的参数:商品的id(sku_id)更新的商品数量(count)
class CartUpdateView(View):
    '''购物车记录更新'''

    def post(self, request):
        '''购物车记录更新'''
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        # 接受数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
            # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
        # 业务处理:更新购物车记录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
        # 更新
        conn.hset(cart_key, sku_id, count)

        #计算用户购物车中商品的总件数{'1':5,'2':3}
        total_count=0
        vals=conn.hvals(cart_key)
        for val in vals:
            total_count+=int(val)
        #范湖应答
        return JsonResponse({'res': 5, 'total_count':total_count,'message': '更新成功'})
def get_cart_count(user):
    '''获取用户购物车购买的商品的总数'''
    #保存用户购物车中商品的总数目
    total_count=0

    if user.is_authenticated():
        #链接redis
        conn=settings.REDIS_CONN
        #key
        cart_key='cart_%d'%user.id\
        #获取信息
        cart_dict=conn.hgetall(cart_key)
        #遍历获取商品的信息
        for sku_id,count in cart_dict.items():
            total_count+=int(count)
        return  total_count


#购物车记录删除
#采用ajax post请求
#前段需要传递的参数:商品的id(sku_id)
#/cart/delete
class CartDetleView(View):
    '''购物车记录删除'''
    def post(self,request):
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})
        #接受参数
        sku_id=request.POST.get('sku_id')
        #数据的校验
        if not sku_id:
            return JsonResponse({'res':1,'errmsg':'无效的商品的id'})
        #校验商品是否存在
        try:
            sku=GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            #商品不存在
            return JsonResponse({'res':2,'errmsg':'商品不存在'})
        #业务处理,删除购物车记录
        conn=settings.REDIS_CONN
        cart_key='cart_%d'%user.id

        #删除hdel
        conn.hdel(cart_key,sku_id)

        # 计算用户购物车中商品的总件数{'1':5,'2':3}
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        #返回应答
        return  JsonResponse({'res':3,'total_count':total_count,'message':'删除成功'})