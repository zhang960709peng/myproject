"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from user import views
from user import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^register_verifyn$', views.Register_verify.as_view(), name='Register_verify'),
    url(r'^validate_code',views.validate_code,name='validate_code'),
    url(r'^email$',views.email,name='email'),
    url(r'^update_password$',views.Update_password.as_view(),name='update_password'),
    url(r'^active/(?P<token>.*)$',views.ActiveView.as_view(),name='active'),
    url(r'^update_password1/(?P<token>.*)$',views.Update_password1.as_view(),name='Update_password1'),
    url(r'^update_password2$',views.Update_password2.as_view(),name='update_password2'),
    url(r'^$',views.User_center_info.as_view(),name='user_center_info'),
    url(r'^user_center_order$',views.User_center_order.as_view(),name='user_center_order'),
    url(r'^user_center_site$',views.User_center_site.as_view(),name='user_center_site'),
    url(r'^user_center_site1$',views.User_center_site1.as_view(),name='user_center_site1'),
    url(r'^user_center_site_handler$',views.User_center_site_handler.as_view(),name='user_center_site_handler'),
    url(r'^place_order$',views.Place_order.as_view(),name='place_order'),
    url(r'^loginout$',views.Loginout.as_view(),name='loginout'),



]
