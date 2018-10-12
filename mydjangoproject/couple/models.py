from django.db import models

class Wife(models.Model):
    name = models.CharField(max_length=100)

class Husband(models.Model):
    name = models.CharField(max_length=100)
    wife = models.OneToOneField(Wife)