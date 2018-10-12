#使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
#创建一个Celery类的实例对象
Celery('celery_tasks.tasks',broker='redis://192.168.12.166:6379/0')
#定义任务函数
@app.task
def send_register_active_email(user_email,user_name,encryption_url):
    subject = '天天生鲜欢迎信息'  # 邮件主题
    message = ''  # 文本内容
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [user_email]  # 收件人
    html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="%s">%s</a>' % (
        user_name, encryption_url, encryption_url)
    print(3)
    send_mail(subject, message, sender, receiver, html_message=html_message)