import datetime

from django.db import models

from project.models import Module


class Case(models.Model):
    """
    测试用例表
    """
    moduleid = models.ForeignKey(Module, on_delete=models.DO_NOTHING, verbose_name='关联模块')  # 数据库的模块管理
    casename = models.CharField(max_length=100, verbose_name='用列名')  # 对应 yaml 用列
    title = models.CharField(max_length=100, verbose_name='用列名称')  # 对应 title 用列
    precondition = models.CharField(max_length=100, null=True, blank=True, verbose_name='前置条件')
    data = models.CharField(max_length=500, null=True, blank=True, verbose_name='测试数据')
    isdone = models.BooleanField(default=False, blank=True, null=True, verbose_name='是否完成')  # 默认未完成
    maintainer = models.CharField(max_length=32, null=True, blank=True, verbose_name='维护者')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
            self.updatetime = datetime.datetime.now()
        super(Case, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name


class LocationType(models.Model):
    """
    定位类型字典表
    """

    location_type = models.CharField(max_length=100, unique=True, verbose_name='定位类型')

    def __str__(self):
        return self.location_type

    def save(self, *args, **kwargs):
        if not self.id:
            self.updatetime = datetime.datetime.now()
        super(LocationType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '定位类型'
        verbose_name_plural = verbose_name


class OperateType(models.Model):
    """
    执行类型字典表
    """

    operate_type = models.CharField(max_length=100, unique=True, verbose_name='定位类型')

    def __str__(self):
        return self.operate_type

    def save(self, *args, **kwargs):
        if not self.id:
            self.updatetime = datetime.datetime.now()
        super(OperateType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '执行类型'
        verbose_name_plural = verbose_name


class CaseSte(models.Model):
    """
    用列步骤表
    """

    caseid = models.ForeignKey(Case, related_name='case_ste', on_delete=models.CASCADE, verbose_name='关联用列')
    casesteid = models.IntegerField(verbose_name='步骤顺序')
    locat_type = models.ForeignKey(LocationType, on_delete=models.SET_NULL,blank=True, null=True, verbose_name='定位类型')
    ope_type = models.ForeignKey(OperateType, on_delete=models.SET_NULL,blank=True, null=True, verbose_name='执行类型')
    locate = models.CharField(max_length=200, verbose_name='定位器')
    info = models.CharField(max_length=200, blank=True, null=True, verbose_name='步骤说明')
    expect = models.CharField(max_length=200, blank=True, null=True, verbose_name='预期结果')

    def __str__(self):
        return self.info

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
            self.updatetime = datetime.datetime.now()
        super(CaseSte, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '用列步骤'
        verbose_name_plural = verbose_name
