from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from three.models import *
from django.core import serializers
import json
# Create your views here.
def three(request):
    return render(request,'three/three.html')
def select_all_province(request):
    province_list=Province.objects.all()
    print(province_list)
    ret={
        'province':serializers.serialize('json',province_list)
    }
    print(ret)
    return JsonResponse(ret)

