from django.shortcuts import render,redirect
from django.core.urlresolvers import  reverse
from django.views.generic import View
from goods.models import GoodsSKU
from django.conf import settings
from user.models import  Address
from util.user_util import LoginRequiredMixin
from django.http import JsonResponse
from order.models import OrderInfo ,OrderGoods
from datetime import datetime
from django.db import transaction
# Create your views here.
class OrderPlaceView(LoginRequiredMixin,View):
    '''提交订单页面显示'''
    def post(self,request):
        '''提交订单页面显示'''
        #获取登录的用户
        user=request.user
        #获取参数sku_ids
        sku_ids=request.POST.getlist('sku_ids')

        #校验参数
        if not sku_ids:
            #跳转到购物车页面
            return redirect(reverse('cart:show'))

        conn=settings.REDIS_CONN
        cart_key='cart_%d'%user.id
        skus=[]
        #保存商品的总件数和总价格
        total_count=0
        total_price=0
        #遍历sku_ids 获取用户要购买的商品的信息
        for sku_id in sku_ids:
            #根据商品的id获取商品的信息
            sku=GoodsSKU.objects.get(id=sku_id)
            #获取用户索要购买商品的数量
            count=conn.hget(cart_key,sku_id)
            #计算商品的小计
            amount=sku.price*int(count)
            #动态给sku增加属性count,保存购买商品的数量
            sku.count=count
            #动态给sku增加属性amount,保存购买商品的小计
            sku.amount=amount
            #追加
            skus.append(sku)
            #累加计算商品的总件数和总价格
            total_count+= int(count)
            total_price+= amount
        #运费 :实际开发的时候,属于一个子系统
        transit_price=10#写死
        #实付款
        total_pay=total_price+transit_price
        #获取用户的收件地址
        addres=Address.objects.filter(user=user)

        #组织上下文
        sku_ids=','.join(sku_ids)
        context={
            'skus':skus,
            'total_count':total_count,
            'total_price':total_price,
            'transit_price':transit_price,
            'total_pay':total_pay,
            'addres':addres,
            'sku_ids':sku_ids
        }

        #使用模板
        return render(request,'dailyfresh/place_order.html',context)

#前段传递的参数:地址id(addr_id)支付方式 pay_method 用户要购买的商品id 字符串(sku_ids)
class OrderCommitView(LoginRequiredMixin,View):
    '''订单创建'''
    @transaction.atomic
    def post(self,request):
        '''订单创建'''
        #判断用户是否登录
        user=request.user
        if not user.is_authenticated():
            return JsonResponse({'res':0,'errmsg':'用户未登录'})

        #接受参数
        addr_id =request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids=request.POST.get('sku_ids')

        #校验参数
        if not all([addr_id,pay_method,sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '参数不完整'})

        #校验支付方式
        if pay_method not in OrderInfo.PAY_METHOD.keys():
            return  JsonResponse({'res': 2, 'errmsg': '非法的支付方式'})
        #校验地址
        try:
            addr=Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            #地址不存在
            return  JsonResponse({'res': 3, 'errmsg': '地址非法'})


        #todo :创建订单核心业务

        #组织参数
        #订单id:年月日时分秒+用户id
        order_id=datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)
        #运费
        transit_price=10
        #总数目和总金额
        total_count=0
        total_price=0
        #设置事务保存点
        save_id=transaction.savepoint()
        try:
            # todo :向df_order_info 中添加一条记录
            order=OrderInfo.objects.create(order_id=order_id,
                                           user=user,
                                           addr=addr,
                                           pay_method=pay_method,
                                           total_count=total_count,
                                           total_price=total_price,
                                           transit_price=transit_price)
            # todo:用户的订单中有几个商品,需要向df_order_goods表中加入几条记录
            conn=settings.REDIS_CONN
            cart_key='cart_%d'%user.id
            sku_ids=sku_ids.split(',')

            for sku_id in sku_ids:
                #获取商品的信息
                try:
                    sku=GoodsSKU.objects.select_for_update().get(id=sku_id)
                except:
                    #商品不存在
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': '商品不存在'})
    
                import time
                time.sleep(10)
                #从redis中获取用户要购买的商品的数量
                count=conn.hget(cart_key,sku_id)

                #todo:判断商品的库存
                if int(count)>sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 6, 'errmsg': '商品的库存不足'})
                #todo:向df_order_goods添加一条记录
                OrderGoods.objects.create(order=order,
                                          sku=sku,
                                          count=count,
                                          price=sku.price)

                #todo:更新商品的库存和销量
                sku.stock-=int(count)
                sku.sales+=int(count)
                sku.save()
                #todo:累加计算订单商品的总数量和总价格
                amount=sku.price*int(count)
                total_count+=int(count)
                total_price+=amount

            #todo:更新订单信息表中商品的总数量和总价格
            order.total_count=total_count
            order.total_price=total_price
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return  JsonResponse({'res': 7, 'errmsg': '下单失败'})
        #提交事务
        transaction.savepoint_commit(save_id)
        #todo:清除用户购物车中对应的记录
        conn.hdel(cart_key,*sku_ids)

        #返回应答
        return JsonResponse({'res': 5, 'message': '创建成功'})


