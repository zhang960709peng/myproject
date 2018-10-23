# 使用celery
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from  django.template import loader,RequestContext
from goods.models import *


# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.12.166:6379/1')


# 定义任务函数
@app.task
def send_register_active_email(subject, message, sender, receiver, html_message):
    send_mail(subject, message, sender, receiver, html_message=html_message)
@app.task
def send_update_password_email(subject, message, sender, receiver, html_message):
    send_mail(subject, message, sender, receiver, html_message=html_message)
@app.task
def task_generate_static_index():
    '''产生首页静态页面'''
    print('生成静态首页begin')
    # 获取商品的种类信息
    goodstype_list = GoodsType.objects.all()
    IndexGoodsBanner_list = IndexGoodsBanner.objects.all().order_by('index')
    IndexPromotionBanner_list = IndexPromotionBanner.objects.all().order_by('index')

    for i in goodstype_list:
        image_set = IndexTypeGoodsBanner.objects.filter(type=i, display_type=1).order_by('index')
        bittle_set = IndexTypeGoodsBanner.objects.filter(type=i, display_type=0).order_by('index')

        i.image_banners = image_set
        i.bittle_banners = bittle_set

    cart_count = 0

    # for i in IndexTypeGoodsBanner_list:
    #     if i.display_type==0:
    #         image_list.append(i)
    #     elif i.display_type==1:
    #         bittle_list.append(i)

    # 准备数据字典
    context = {
        'goodstype_list': goodstype_list,
        'IndexGoodsBanner_list': IndexGoodsBanner_list,
        'IndexPromotionBanner_list': IndexPromotionBanner_list,
        'cart_count': cart_count
    }

    #使用模板
    #1.加载模板文件，返回模板对象
    temp=loader.get_template('dailyfresh/static_index.html')

    #2.模板渲染
    static_index_html = temp.render(context)

    #生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR,'static/html/index.html')
    with open(save_path,'w')as f:
        f.write(static_index_html)

# @app.task
# def send_update_password_email(subject, message, sender, receiver, html_message):
#     send_mail(subject, message, sender, receiver, html_message=html_message)
