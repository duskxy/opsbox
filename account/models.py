from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLES = (
        ('developer_supremo', '总监'),
        ('developer_manager', '经理'),
        ('developer', '研发'),
        ('test', '测试'),
        ('sa',"系统管理员")
    )
    username = models.CharField(max_length=20,unique=True,verbose_name="用户名")
    email = models.CharField(max_length=50,verbose_name="邮箱")
    role = models.CharField(max_length=20,choices=ROLES,verbose_name="角色")
    leader = models.ForeignKey("self",null=True,blank=True,default="",on_delete=models.SET_NULL,verbose_name="上级主管")

    class Meta:
        db_table = "user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
