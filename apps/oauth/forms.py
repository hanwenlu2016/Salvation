# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from .models import Users
from util.rephone import is_phone


class SignUpForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    password1 = forms.CharField(label='password1')
    password2 = forms.CharField(label='password2')

    class Meta:
        model = Users
        fields = ('username', 'email', 'mobile')

    def clean_mobile(self):
        """
        验证手机号码合法性
        :return:
        """
        mobile = self.cleaned_data.get("mobile")
        is_exist = Users.objects.filter(mobile=mobile).count()
        if is_exist >= 1:
            raise forms.ValidationError("手机号码已经存在！！")
        elif not is_phone(str(mobile)):
            raise forms.ValidationError("手机号码格式错误！！")
        return mobile

    def clean_password2(self):
        """
        验证2次密码合法性
        :return:
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不一致")
        return password1

    def save(self, commit=True):
        """
        保存登录表单
        :param commit:
        :return:
        """
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='密码')

    class Meta:
        model = Users
        # exclude = ['last_login', 'date_joined', 'first_name','last_name','objects']
        # fields = '__all__'
        fields = (
            'username', 'password', 'is_superuser', 'is_staff', 'email', 'name', 'gender', 'mobile', 'birthday', 'dep',
            'post',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserCreateForm, self).__init__(*args, **kwargs)

    def clean_mobile(self):
        """
        验证手机号码合法性
        :return:
        """
        mobile = self.cleaned_data.get("mobile")
        is_exist = Users.objects.filter(mobile=mobile).count()
        if is_exist >= 1:
            raise forms.ValidationError("手机号码已经存在！！")
        elif not is_phone(str(mobile)):
            raise forms.ValidationError("手机号码格式错误！！")
        return mobile

    def clean_email(self):
        """
        验证email合法性
        :return:
        """
        email = self.cleaned_data.get("email")
        is_exist = Users.objects.filter(email=email).count()
        if is_exist >= 1:
            raise forms.ValidationError("邮箱已经存在！！")
        return email

    def save(self, commit=True):
        """
        保存登录表单
        :param commit:
        :return:
        """
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):


    class Meta:
        model = Users
        # exclude = ['last_login', 'date_joined', 'first_name','last_name','objects']
        # fields = '__all__'
        fields = (
            'username', 'is_superuser', 'is_staff', 'email', 'name', 'gender', 'mobile', 'birthday', 'dep', 'post',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    def clean_mobile(self):
        """
        验证手机号码合法性
        :return:
        """
        mobile = self.cleaned_data.get("mobile")
        mobile_old = self.initial.get("mobile")
        if mobile == mobile_old:  # 如果更新数据等于旧数据
            return mobile
        elif mobile != mobile_old:  # 如果当前数据不等于旧数需要验证合法性
            is_exist = Users.objects.filter(mobile=mobile).count()
            if is_exist >= 1:
                raise forms.ValidationError("手机号码已经存在！！")
        else:  # 号码不合法
            raise forms.ValidationError("手机号码格式错误！！")
        return mobile

    def clean_email(self):
        """
        验证email合法性
        :return:
        """
        email = self.cleaned_data.get("email")
        email_old = self.initial.get("email")
        if email == email_old:  # 如果更新数据等于旧数据
            return email
        else:
            is_exist = Users.objects.filter(email=email).count()
            if is_exist >= 1:
                raise forms.ValidationError("邮箱已经存在！！")
        return email

    def save(self, commit=True):
        """
        保存登录表单
        :param commit:
        :return:
        """
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
        return user
