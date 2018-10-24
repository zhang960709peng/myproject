from django.contrib import admin
from goods.models import *
from django.core.cache import cache

class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中数据时调用'''
        super().save_model(request,obj,form,change)
        #
        # #发出任务,让celery worker重新生成首页静态页
        from celery_tasks.tasks import task_generate_static_index
        task_generate_static_index.delay()
        cache.delete("cache_index")
        # print("save_model....")

    def delete_model(self, request, obj):
        '''删除表中数据时调用'''
        super().delete_model(request,obj)
        #
        # #发出任务,让celery worker重新生成首页静态页
        from celery_tasks.tasks import task_generate_static_index
        task_generate_static_index.delay()
        cache.delete("cache_index")
class GoodsTypeAdmin(BaseAdmin):
    pass
class GoodsAdmin(BaseAdmin):
    pass
class GoodsSKUAdmin(BaseAdmin):
    pass
class GoodsImageAdmin(BaseAdmin):
    pass
class IndexGoodsBannerAdmin(BaseAdmin):
    pass
class IndexPromotionBannerAdmin(BaseAdmin):
    pass
class IndexTypeGoodsBannerAdmin(BaseAdmin):
    pass

admin.site.register(GoodsType,GoodsTypeAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(GoodsImage,GoodsImageAdmin)
admin.site.register(IndexGoodsBanner,IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)
