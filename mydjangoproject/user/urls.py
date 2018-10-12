from django.conf.urls import include, url
from django.contrib import admin
from user import views

urlpatterns = [
    url(r'^areas$', views.select_all_area,name="select_all_area"),
    url(r'^area/(\d+)$', views.select_area_by_id,name="select_area_by_id"),
    url(r'^user_name_handler',views.user_name_handler,name='user_name_handler'),
    url(r'^register$', views.register,name="register"),
    url(r'^register_handler$', views.register_handler,name="register_handler"),
    url(r'^login$', views.login, name="login"),
    url(r'^login_handler$', views.login_handler, name="login_handler"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^modify_pwd$', views.modify_pwd, name="modify_pwd"),
    url(r'^modify_pwd_handler$', views.modify_pwd_handler, name="modify_pwd_handler"),
    url(r'^validate_code$', views.validate_code, name="validate_code"),



    url(r'^set_cookie$', views.set_cookie, name="set_cookie"),
    url(r'^get_cookie$', views.get_cookie, name="get_cookie"),


    url(r'^set_session$', views.set_session, name="set_session"),
    url(r'^get_session$', views.get_session, name="get_session"),
    url(r'^del_session$', views.del_session, name="del_session"),
    url(r'^variable$', views.variable, name="variable"),
]
