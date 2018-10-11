from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Create your models here.


"""
继承ＡｂｓｔｒａｃｔＵｓｅｒ：使用他的属性
继承BaseModel：共有的属性
"""


class User(AbstractUser,BaseModel):
    """用户模型类"""
    class Meta:
        db_table='df_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name