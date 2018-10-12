from django.db import models



"""
实体类
"""
class BookInfo(models.Model):
    btitle = models.CharField(max_length=100)
    bpubdate = models.DateTimeField(null=True)
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(default=0)
    isdelete = models.BooleanField(default=False)



    def __str__(self):
        return "BooInfo(btitle=%s)"%self.btitle

    class Meta:
        verbose_name="书"
        verbose_name_plural="书"

class HeroInfo(models.Model):
    hname = models.CharField(max_length=100,verbose_name="姓名")
    hgender = models.BooleanField(verbose_name="性别")
    hcontent = models.TextField()
    hbookinfo = models.ForeignKey(BookInfo)
    hpic = models.ImageField(upload_to="images/",null=True)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return "HeroInfo(hname=%s)"%self.hname

    def sex(self):
        if self.hgender:
            return "男"
        else:
            return "女"

    sex.short_description = "性别"

    class Meta:
        verbose_name="英雄人物"
        verbose_name_plural="英雄人物"
        ordering = ["-id","hname"]


