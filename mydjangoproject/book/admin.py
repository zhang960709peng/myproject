from django.contrib import admin
from book.models import *

"""
注册实体类：管理界面
"""
# class BookInfoInline(admin.TabularInline):
# # class BookInfoInline(admin.StackedInline):
#     model = HeroInfo
#     extra = 1
#
# class HeroInfoAmin(admin.ModelAdmin):
#     """管理类"""
#     #列表页面-显示字段
#     list_display = ["id","hname","sex"]
#     #过滤
#     list_filter = ["hname"]
#     #搜索
#     search_fields = ["hname"]
#     #分页
#     list_per_page = 2
#     #详情页面-显示字段
#     # fields = ["hcontent","hname"]
#     #情页面-显示字段分组
#     # fieldsets = [
#     #     ("group1",{"fields":["hname","hgender"]}),
#     #     ("group2",{"fields":["hcontent","hbookinfo"]})
#     # ]
#
#
# class BookInfoAmin(admin.ModelAdmin):
#     """管理类"""
#     #列表页面-显示字段
#     list_display = ["id","btitle"]
#     #关联类
#     inlines = [BookInfoInline]
#
#
#
# admin.site.register(HeroInfo,HeroInfoAmin)
# admin.site.register(BookInfo,BookInfoAmin)
#







admin.site.register(BookInfo)
admin.site.register(HeroInfo)