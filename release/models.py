from django.db import models
from account.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=20,unique=True,verbose_name="项目名称")
    desc = models.TextField(max_length=50,default='',null=True,blank=True,verbose_name="备注")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        db_table = "project"
        verbose_name = "项目"
        verbose_name_plural = verbose_name

class Web(models.Model):
    projectname = models.ForeignKey(Project,null=True,blank=True,on_delete=models.SET_NULL,verbose_name="项目")
    name = models.CharField(max_length=20,verbose_name="web名称")
    desc = models.TextField(max_length=50,default='',null=True,blank=True,verbose_name="备注")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = "web"
        verbose_name = "web工程"
        verbose_name_plural = verbose_name

class Deploy(models.Model):

    STATUS = (
        (0, u'申请'),
        (1, u'已审核'),
        (2, u'上线'),
        (3, u'取消上线'),
    )
    projectname = models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE,related_name="project_dep",verbose_name="项目名称")
    webname = models.ForeignKey(Web,null=True,blank=True,on_delete=models.CASCADE,related_name="web_dep",verbose_name="web名称")
    version = models.CharField(max_length=20,verbose_name="项目版本")
    info = models.CharField(max_length=100,verbose_name="版本描述")
    applicant = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="申请人")
    reviewer = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="reviewer",verbose_name="审核人")
    assign_to = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="assignd",verbose_name="上线人")
    status = models.IntegerField(default=0,choices=STATUS,verbose_name="上线状态")
    console_output = models.TextField(default='',verbose_name="上线输出结果")
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name=u'申请时间')
    deploy_time = models.DateTimeField(auto_now=True, verbose_name=u'上线完成时间')

    class Meta:
        db_table = "deploy"
        verbose_name = "发布列表"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.version