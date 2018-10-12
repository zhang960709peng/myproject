from django.conf.urls import include, url
from django.contrib import admin
from book import views
"""
这里一定加$
"""
urlpatterns = [
    url(r'^$', views.index,name="index"),
    url(r'^books$', views.book_select_all, name="book_select_all"),
    url(r'^book/(?P<bid>\d+)$', views.book_select_by_id, name="book_select_by_id"),

    url(r'^heroinfos2$', views.hero_select_all2, name="hero_select_all2"),

    url(r'^heroinfos$', views.hero_select_all, name="hero_select_all"),
    url(r'^heroinfo/(?P<hid>\d+)$', views.hero_select_by_id, name="hero_select_by_id"),

    url(r'^heroinfo/edit$', views.hero_edit,name="hero_edit"),
    url(r'^heroinfo/edit_handler$', views.hero_edit_handler,name="hero_edit_handler"),

    url(r'^heroinfo/delete1$', views.hero_delete1,name="hero_delete1"),
    url(r'^heroinfo/delete2$', views.hero_delete2,name="hero_delete2"),

    url(r'^heroinfo/insert$', views.hero_insert, name="hero_insert"),
    url(r'^heroinfo/insert_handler$', views.hero_insert_handler, name="hero_insert_handler"),

    url(r'^heroinfos/page$', views.hero_page, name="hero_page"),
    url(r'^heroinfo_search$', views.heroinfo_search, name="heroinfo_search"),
    url(r'^heroinfo_search_handler$', views.heroinfo_search_handler, name="heroinfo_search_handler"),
    # url(r'^heroinfos/page$', views.hero_page, name="hero_page"),


    url(r'^test$', views.test,name="test"),

    url(r'^test1$', views.test1,name="test1"),
    url(r'^test2$', views.test2),
    url(r'^test3$', views.test3),

    url(r'^test4$', views.test4),

    url(r'^test5$', views.test5),
    url(r'^test6$', views.test6),

    url(r'^test7$', views.test7),

    url(r'^test7_1$', views.test7_1,name="test7_1"),
    url(r'^test7_2$', views.test7_2,name="test7_2"),

    url(r'^test8$', views.test8),
    url(r'^test10$', views.test10),
    url(r'^test11$', views.test11),
    url(r'^test12$', views.test12),
]



