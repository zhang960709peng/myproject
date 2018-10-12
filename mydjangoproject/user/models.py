
from django.db import models



class User(models.Model):
    name = models.CharField(max_length=100,unique=True,null=False)
    pwd = models.CharField(max_length=32,null=False)

    def get_name(self):
        return self.name

    class Meta:
        db_table = 't_user'



class Area(models.Model):
    name = models.CharField(max_length=100,unique=True)
    parent = models.ForeignKey("self",db_column="pid",null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_area'