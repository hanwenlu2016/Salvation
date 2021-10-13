import datetime

from django.db import models
from django.urls import reverse

from oauth.models import Users


class DeployInfo(models.Model):
    """
    部署表
    """
    prjname = models.CharField(max_length=100, unique=True, verbose_name='部署名称')
    prjalias = models.CharField(max_length=32,  verbose_name='项目别名')
    deploypath = models.CharField(max_length=200,  verbose_name='部署路径')
    depldescr = models.TextField(null=True, blank=True, verbose_name='部署描述')

    def __str__(self):
        return self.prjname

    def get_absolute_url(self):
        return reverse('devlist')

    class Meta:
        verbose_name = '部署信息'
        verbose_name_plural = verbose_name


class Project(models.Model):
    """
    项目表
    """

    project_name = models.CharField(max_length=100, unique=True, verbose_name='项目名称')
    isenabled = models.BooleanField(default=True, verbose_name='项目状态')
    descr = models.TextField(null=True, blank=True, verbose_name='项目描述')
    version = models.CharField(max_length=32, null=True, blank=True, editable=True, verbose_name='版本版本')
    deployinfos = models.ForeignKey(DeployInfo, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='部署信息')

    prjcet_personliable = models.ForeignKey(Users, null=True, blank=True, on_delete=models.SET_NULL,related_name='user_prjcet',
                                           verbose_name='所属负责人', )

    prjcet_participant = models.ManyToManyField(Users,  blank=True,verbose_name='项目参与者', )

    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    creator = models.CharField(max_length=32, verbose_name='创建人')
    updater = models.CharField(max_length=32, null=True, blank=True,verbose_name='更新人')


    def save(self, *args, **kwargs):

        if not self.id:
            self.createtime = datetime.datetime.now()
            self.updatetime = datetime.datetime.now()

        super(Project,self).save(*args, **kwargs)

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse('prlist')

    class Meta:
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name


class Module(models.Model):
    """
    功能模块表
    """
    projcet = models.ForeignKey(Project, null=True, blank=True,verbose_name='所属项目', on_delete=models.SET_NULL)
    module_name = models.CharField(max_length=32, verbose_name='模块名称')
    module_alias = models.CharField(max_length=32, verbose_name='模块别名')  # 此别名对应Case表中的modelname
    isenabled = models.BooleanField(default=True, verbose_name='状态')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    maintainer = models.CharField(max_length=32, verbose_name='维护者')

    def __str__(self):
        return self.module_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
            self.updatetime = datetime.datetime.now()

        super(Module,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('modulelist')

    class Meta:
        verbose_name = '功能模块'
        verbose_name_plural = verbose_name
