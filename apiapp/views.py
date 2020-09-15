from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from apiapp.models import Employee
from apiapp.serializers import EmployeeSerializer, EmployeeDeSerializer


class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
        查询接口
        :param request:
        :return:
        """
        user_id = kwargs.get('id')
        if user_id:
            emp_obj = Employee.objects.filter(id=user_id).first()
            if emp_obj:
                emp_dict = EmployeeSerializer(emp_obj).data

                return Response({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": emp_dict,
                })
            else:
                return Response({
                    "status": 500,
                    "message": "查询单个用户失败",
                })

        else:
            emp_all = Employee.objects.all()
            data_all = EmployeeSerializer(emp_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询所有用户成功",
                "results": data_all,
            })

    def post(self, request, *args, **kwargs):
        """
        添加数据
        :param request:
        :return:
        """
        user_data = request.data
        if not isinstance(user_data, dict) or user_data == {}:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "数据格式有误"
            })
        serializer = EmployeeDeSerializer(data=user_data)
        if serializer.is_valid():
            emp_obj = serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "用户保存成功",
                "results": EmployeeSerializer(emp_obj).data
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors
        })
