from django.db import models
from bases.models import Buildings

from django.contrib.auth.models import AbstractUser

#自定義用戶
class User(AbstractUser):
    building = models.ForeignKey(Buildings,verbose_name='大廈名稱', on_delete=models.CASCADE,blank=True,null=True) 

    class Meta:
        db_table = 'auth_user'
        verbose_name = "用戶"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.username