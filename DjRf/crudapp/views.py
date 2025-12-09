from django.shortcuts import render,HttpResponse
from crudapp.models import *
from crudapp.serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def get_data(request):
    try : 
        emps = Employee.objects.all()
        ser = EmployeeSerializer(emps,many=True)
        return Response({"Data":ser.data},status=status.HTTP_200_OK)
    except Exception as e :
        return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def add_data(request):
    try:
        ser = EmployeeSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"errors":ser.errors,"message":"Somethong went wrong"},status=status.HTTP_400_BAD_REQUEST)
        else:
            ser.save()
            return Response({"data":ser.data},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_data_id(request,id):
    try:
        emp = Employee.objects.get(pk=id)
        ser = EmployeeSerializer(emp)
        return Response({"data":ser.data},status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"message": "Employee not found", "errors": f"No employee found with id {id}"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_data(request,id):
    try:
        emp = Employee.objects.get(pk=id)
        ser = EmployeeSerializer(emp,data=request.data)

        if not ser.is_valid():
            return Response({"errors":ser.errors,"message":"Somethong went wrong"},status=status.HTTP_400_BAD_REQUEST)
        else:
            ser.save()
            return Response({"data":ser.data},status=status.HTTP_201_CREATED)
    except Employee.DoesNotExist:
        return Response(
            {"message": "Employee not found", "errors": f"No employee found with id {id}"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_data(request,id):
    try:
        emp = Employee.objects.get(pk=id)
        emp.delete()
        return Response({"message":"Employee deleted"},status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"message": "Employee not found", "errors": f"No employee found with id {id}"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"message":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)