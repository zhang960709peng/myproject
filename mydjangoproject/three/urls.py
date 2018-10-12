from django.conf.urls import include, url
from django.contrib import admin
from three import views
"""
这里一定加$
"""
urlpatterns = [
    url(r'^three$', views.three,name="three"),
    url(r'^select_all_province$', views.select_all_province,name="select_all_province"),

]



