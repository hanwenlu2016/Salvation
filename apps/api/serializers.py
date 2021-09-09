# -*- coding: utf-8 -*-
# @File: serializers.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/9/7  15:17


from rest_framework import serializers

from element.models import Case, LocationType, OperateType, CaseSte
from project.models import Module,Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目序列化类
    """

    class Meta:
        model = Project

        fields =('id','project_name','isenabled','version')


class ModuleSerializer(serializers.ModelSerializer):
    """
    模块序列化类 list
    """
    updatetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Module
        fields = ("id", "projcet", "module_name","module_alias",  "isenabled", "updatetime", "maintainer",)


class LocationTypeSerializer(serializers.ModelSerializer):
    """
    定位类型序列化
    """

    class Meta:
        model = LocationType
        fields = "__all__"

class OperateTypeSerializer(serializers.ModelSerializer):
    """
    操作类型序列化
    """

    class Meta:
        model = OperateType
        fields = "__all__"

class CaseSteSerializer(serializers.ModelSerializer):
    """
    用列步骤序列化 list
    """
    locat_type = serializers.ReadOnlyField(source='locat_type.location_type')  # 定位类型
    ope_type = serializers.ReadOnlyField(source='ope_type.operate_type')  # 操作类型

    class Meta:
        model = CaseSte
        fields = (
            "id", "casesteid", "locat_type", "ope_type", "locate", "info", "expect")

class CaseListSerializer(serializers.ModelSerializer):
    """
    用列序列化 list
    """
    moduleid = serializers.ReadOnlyField(source='moduleid.module_name')  # 关联模块
    case_ste = CaseSteSerializer(many=True, )  # 用列步骤 引用CaseSteSerializer
    updatetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Case
        fields = (
            "id", "moduleid","title", "casename","precondition", "case_ste", "data", "isdone", "maintainer",
            "updatetime")

class CaseSerializer(serializers.ModelSerializer):
    """
    用列序列化 crae
    """

    moduleid = serializers.PrimaryKeyRelatedField(required=True, queryset=Module.objects.all(),label="所属模块")
    case_ste = CaseSteSerializer(many=True, )  # 用列步骤 引用CaseSteSerializer

    maintainer = serializers.HiddenField(default=serializers.CurrentUserDefault())  #隐藏此字段并提交当前用户  *未用

    class Meta:
        model = Case
        fields = (
            "id", "moduleid", 'casename', "title", "precondition",  "case_ste","isdone","data", "updatetime", "maintainer",)


    def create(self, validated_data):
        """
       插入case用列表 和 caseste步骤表关联数据
       """
        # 移除case表数据
        cases_data = validated_data.pop('case_ste')
        # 插入case表数据
        validated_data["maintainer"] = self.context["request"].user
        case = Case.objects.create(**validated_data)

        # 循环出外键数据
        for case_data in cases_data:
            CaseSte.objects.create(caseid=case, **case_data)
        return case


    def update(self, instance, validated_data):
        """
        更新操作
        """
        cases_data = validated_data.pop('case_ste')
        caseste = (instance.case_ste).all()

        caseste = list(caseste)

        # 更新 Case 用列表数据
        # super(CaseSerializer, self).update(instance, validated_data)
        instance.moduleid = validated_data.get('moduleid', instance.moduleid)
        instance.casename = validated_data.get('casename', instance.casename)
        instance.title = validated_data.get('title', instance.title)
        instance.precondition = validated_data.get('precondition', instance.precondition)
        instance.isdone = validated_data.get('isdone', instance.isdone)
        instance.save()

        # 更新 CaseSte 步骤表数据
        for case_data in cases_data:
            ste = caseste.pop(0)
            ste.casesteid = case_data.get('casesteid', ste.casesteid)
            ste.locat_type = case_data.get('types', ste.locat_type)
            ste.ope_type = case_data.get('operate', ste.ope_type)
            ste.locate = case_data.get('locate', ste.locate)
            ste.info = case_data.get('info', ste.info)
            ste.expect = case_data.get('expect', ste.expect)
            ste.save()
        return instance


