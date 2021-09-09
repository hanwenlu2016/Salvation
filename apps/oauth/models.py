from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
    dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name='部门')
    post = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, verbose_name='职位')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('userlist')


    # 自动生成token
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['-id']
