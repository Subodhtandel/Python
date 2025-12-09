from django.shortcuts import render,HttpResponse
from rest_framework.decorators import api_view,APIView
from myapp.models import *
from rest_framework.response import Response
from myapp.serializer import *
@api_view(['GET'])
def get_users(request):
    return HttpResponse("GET API CALLING")

@api_view(['POST'])
def post_users(request):
    return HttpResponse("POST API CALLING")

@api_view(['PUT'])
def put_users(request):
    return HttpResponse("PUT API CALLING")

@api_view(['DELETE'])
def delete_users(request):
    return HttpResponse("DELETE API CALLING")

# @api_view(['GET'])
# def test(request):
#     return HttpResponse("")
class StudentView(APIView):

    def get(self,request):
        allstudents = Student.objects.all()
        students =  StudentSerializer(allstudents,many=True)
        return Response({"students":students.data})
    
    def post(self,request):
            data = StudentSerializer(data = request.data)
            if not data.is_valid():
                return Response({"Errors":data.errors,"message":"somethng went wrong"})
            else:
                data.save()
                return Response({"Data":data.data,"message":"Data inserted successfully"})
            
class StudentViewId(APIView):

    def get(self,request,id):
        student = Student.objects.get(pk=id)
        ser = StudentSerializer(student)
        return Response({"data":ser.data})
    
    def put(self,request,id):
        student = Student.objects.get(pk=id)
       
        ser= StudentSerializer(student,data=request.data)
        if not ser.is_valid():
            return Response({"Errors":ser.errors,"message":"Something went wrong"})
        else:
            ser.save()
            return Response({"data":ser.data,"message":"data updated successfully"})
        
    def patch(self,request,id):
        student = Student.objects.get(pk=id)
       
        ser= StudentSerializer(student,data=request.data,partial=True)
        if not ser.is_valid():
            return Response({"Errors":ser.errors,"message":"Something went wrong"})
        else:
            ser.save()
            return Response({"data":ser.data,"message":"data updated successfully"})
        
    def delete(self,request,id):
        student = Student.objects.get(pk=id)
        student.delete()
        return Response({"message":"Data deleted"})