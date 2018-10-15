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
# Create your views here.
class Index(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'dailyfresh/index.html')