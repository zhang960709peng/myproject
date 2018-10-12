from django.db import models

class Province(models.Model):
    pname=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.pname
class City(models.Model):
    pname=models.CharField(max_length=100,unique=True)
    cprovince=models.ForeignKey(Province)
    def __str__(self):
        return self.pname
class Area(models.Model):
    pname=models.CharField(max_length=100,unique=True)
    acity=models.ForeignKey(City)
    def __str__(self):
        return self.pname
# Create your models here.
