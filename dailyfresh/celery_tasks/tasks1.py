# 使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()
# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.12.166:6379/3')


# 定义任务函数
# @app.task
# def send_register_active_email(subject, message, sender, receiver, html_message):
#     send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def send_update_password_email(subject, message, sender, receiver, html_message):
    send_mail(subject, message, sender, receiver, html_message=html_message)
