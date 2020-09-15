from rest_framework import serializers
from rest_framework import exceptions

# 每个模型需要单独定义一个序列化器
from apiapp.models import Employee
from drf_03 import settings


class EmployeeSerializer(serializers.Serializer):
    """
    需要为每一个模型单独定制一个序列化类
    在序列化器中定义的序列化的字段名称在model中必须存在
    """
    username = serializers.CharField()
    password = serializers.CharField()
    gender = serializers.IntegerField()
    pic = serializers.ImageField()

    # 定义models中不存在的字段  SerializerMethodField()
    # 自定义字段  返回一个盐
    salt = serializers.SerializerMethodField()

    # 自定义字段属性名可以随意写 但是为字段提供值的方法名必须是 get_字段名
    # 自定义字段在数据库中没有对应的值，所以需要此方法为自定义字段提供值
    # get_字段名：该方法是为salt字段提供值的  self是当前使用的序列化器  obj 是当前的对象
    def get_salt(self, obj):
        return "salt"

    # 自定义性别字段的返回值
    gender = serializers.SerializerMethodField()

    # self: 当前序列化器 obj：当前对象
    def get_gender(self, obj):
        print(type(obj.gender))
        if obj.gender == 0:
            return "male"
        # 性别是choices类型 get_字段名_display()访问对相应的值
        return obj.get_gender_display()

    # 自定义图片返回的全路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        print(obj.pic)
        # http://127.0.0.1:8000/media/pic/1111.jpg
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, obj.pic)


class EmployeeDeSerializer(serializers.Serializer):
    """
    反序列化：将前端提交的数据保存入库
    1. 前端需要提供哪些字段
    2. 对前端提供数据做安全校验
    3. 哪些字段需要一些额外的安全校验
    反序列化是不存在自定义字段的
    """
    # 可以在字段中添加校验规则
    username = serializers.CharField(
        max_length=8,
        min_length=2,
        # 为规则自定义错误信息
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了"
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField(min_length=11, required=True)

    # 自定义字段  重复密码
    # re_pwd = serializers.CharField()

    # TODO 在create保存对象之前  DRF提供了两个钩子函数来对数据进行校验

    # 局部钩子： 可以对反序列化中的某个字段进行校验
    # validate_想验证的字段名
    def validate_username(self, value):
        if "a" in value:
            raise exceptions.ValidationError("用户名有误")

        return value

    # # 全局钩子  可以通过attrs获取到所有的参数
    # def validate(self, attrs):
    #     pwd = attrs.get("password")
    #     re_pwd = attrs.pop("re_pwd")
    #     # 自定义校验规则  两次密码不一致  则无法保存对象
    #     if pwd != re_pwd:
    #         raise exceptions.ValidationError("两次密码不一致")
    #     return attrs

    def create(self, validated_data):
        """
        在保存用户对象时需要重写此方法完成保存
        :param validated_data: 前端传递的需要保存的数据
        :return:
        """
        # print(validated_data)
        return Employee.objects.create(**validated_data)