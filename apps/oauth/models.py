from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class Department(models.Model):
    """
    部门表
    """
    dep_name = models.CharField(max_length=32, verbose_name='部门名称')

    def __str__(self):
        return self.dep_name

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name


class Position(models.Model):
    """
    职位表
    """
    post_name = models.CharField(max_length=32, verbose_name='职位名称')

    def __str__(self):
        return self.post_name

    class Meta:
        verbose_name = "职位"
        verbose_name_plural = verbose_name


class Users(AbstractUser):
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male", verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True,verbose_name='部门')
    post = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, verbose_name='职位')

    def __str__(self):
        return self.username


    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['-id']
