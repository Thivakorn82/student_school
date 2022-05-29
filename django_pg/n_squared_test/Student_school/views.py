from dataclasses import dataclass
from functools import partial
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import viewsets

from Student_school.models import Schools,Students
from Student_school.serializers import SchoolSerializer,StudentSerializer
# Create your views here.

class GetOrCreateStudentsViewSet(viewsets.ModelViewSet):
    def GetStudents(self,req):
        ################################ SERIALIZER ################################
        getStudent = Students.objects.all()
        getStudent_serializer = StudentSerializer(getStudent,many=True)
        return JsonResponse(getStudent_serializer.data,safe=False)

    def PostStudent(self,req):
        ################################ DESERIALIZER ################################
        student_data = JSONParser().parse(req)
        student_serializer = StudentSerializer(data=student_data)
        getSchool = Schools.objects.get(id = student_data['school'])
        getSchool_serializer = SchoolSerializer(getSchool)

        ################################ CHECK_MAX_STUDENT ################################
        MaxStudent = getSchool_serializer.data['max_students']
        CountStudent = Students.objects.filter(school_id = student_data['school']).count()
        if(CountStudent + 1 > MaxStudent):
            return HttpResponse("Too many student for this school!!")

        ################################ CHECK_OBJECT_VALID ################################
        if(student_serializer.is_valid()):
            student_serializer.save()
            return HttpResponse("Student saved")
        else:
            print(student_serializer.errors)
            return HttpResponse("Fail to saved")

class GetOrEditByStudentsIDViewSet(viewsets.ModelViewSet):
    def GetStudentByID(self,req,id):
        ################################ SERIALIZER ################################
        getStudent = Students.objects.get(id=id)
        getStudent_serializers = StudentSerializer(getStudent)
        return JsonResponse(getStudent_serializers.data,safe=False)

    def UpdateStudent(self,req,id):
        if(req.method == "PUT"):
        ################################ DESERIALIZER ################################
            getStudent = Students.objects.get(id=id)
            student_data = JSONParser().parse(req)
            student_serializer = StudentSerializer(getStudent,data=student_data)

        ################################ CHECK_OBJECT_VALID ################################
            if(student_serializer.is_valid()):
                student_serializer.save()
                return HttpResponse("Student updated")
            else:
                print(student_serializer.errors)
                return HttpResponse("update failed")

        elif(req.method == "PATCH"):
        ################################ DESERIALIZER ################################
            getStudent = Students.objects.get(id=id)
            student_data = JSONParser().parse(req)
            student_serializer = StudentSerializer(getStudent,data=student_data,partial=True)

        ################################ CHECK_OBJECT_VALID ################################
            if(student_serializer.is_valid()):
                student_serializer.save()
                return HttpResponse("Student updated")
            else:
                print(student_serializer.errors)
                return HttpResponse("update failed")

    def DeleteStudent(self,req,id):
        getStudent = Students.objects.get(id=id)
        getStudent.delete()
        return HttpResponse("delete student successfully")

class GetOrPostSchoolViewSet(viewsets.ModelViewSet):
    def GetSchool(self,req):
        ################################ SERIALIZER ################################
        getSchool = Schools.objects.all()
        getSchool_serializer = SchoolSerializer(getSchool,many=True)
        return JsonResponse(getSchool_serializer.data,safe=False)

    def PostSchool(self,req):
        school_data = JSONParser().parse(req)
        ################################ CHECK_MAX_STUDENT ################################
        if(school_data['max_students'] < 0):
            return HttpResponse("Max_students must be positive number")

        ################################ SERIALIZER ################################
        school_serializer = SchoolSerializer(data=school_data)

        ################################ CHECK_OBJECT_VALID ################################
        if(school_serializer.is_valid()):
            school_serializer.save()
            return HttpResponse("School saved")
        else:
            print(school_serializer.errors)
            return HttpResponse("Fail to saved")

class GetOrEditBySchoolIDViewSet(viewsets.ModelViewSet):
    def GetSchoolByID(self,req,id):
        ################################ SERIALIZER ################################
        getSchool = Schools.objects.get(id = id)
        getSchool_serializer = SchoolSerializer(getSchool)
        return JsonResponse(getSchool_serializer.data,safe=False)

    def UpdateSchool(self,req,id):
        getSchool = Schools.objects.get(id = id)
        if(req.method == "PUT"):
        ################################ DESERIALIZER ################################
            school_data = JSONParser().parse(req)
            school_serializer = SchoolSerializer(getSchool,data=school_data)

        ################################ CHECK_OBJECT_VALID ################################
            if(school_serializer.is_valid()):
                school_serializer.save()
                return HttpResponse("School updated")
            else:
                print(school_serializer.errors)
                return HttpResponse("update failed")

        elif(req.method == "PATCH"):
        ################################ DESERIALIZER ################################
            school_data = JSONParser().parse(req)
            school_serializer = SchoolSerializer(getSchool,data=school_data,partial=True)
        ################################ CHECK_OBJECT_VALID ################################
            if(school_serializer.is_valid()):
                school_serializer.save()
                return HttpResponse("School updated")
            else:
                print(school_serializer.errors)
                return HttpResponse("update failed")

    def DeleteSchool(self,req,id):
        getSchool = Schools.objects.get(id = id)
        getSchool.delete()
        return HttpResponse("delete school successfully")

class GetOrPostStudentBySchoolIDViewSet(viewsets.ModelViewSet):
    def GetStudentBySchoolID(self,req,id):
        ################################ SERIALIZER ################################
        getStudent = Students.objects.filter(school = id)
        getStudent_serializer = StudentSerializer(getStudent,many=True)
        return JsonResponse(getStudent_serializer.data,safe=False)

    def PostStudentBySchoolID(self,req,id):
        ################################ DESERIALIZER ################################
        student_data = JSONParser().parse(req)
        getSchool = Schools.objects.get(id = id)
        getSchool_serializer = SchoolSerializer(getSchool)

        ################################ CHECK_MAX_STUDENT ################################
        MaxStudent = getSchool_serializer.data['max_students']
        CountStudent = Students.objects.filter(school_id = id).count()
        if(CountStudent + 1 > MaxStudent):
            return HttpResponse("Too many student for this school!!")

        ################################ DESERIALIZER ################################
        student_data['school'] = id
        student_serializer = StudentSerializer(data=student_data)

        ################################ CHECK_OBJECT_VALID ################################
        if(student_serializer.is_valid()):
            student_serializer.save()
            return HttpResponse("Student saved")
        else:
            print(student_serializer.errors)
            return HttpResponse("Fail to saved")

class GetOrEditStudentByIDViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    def GetStudentByID_And_SchoolID(self,req,schools_pk=None,pk=None):
        ################################ SERIALIZER ################################
        getStudent = Students.objects.get(id = pk,school = schools_pk)
        getStudent_serializer = StudentSerializer(getStudent)
        return JsonResponse(getStudent_serializer.data,safe=False)

    def UpdateStudentByID_AND_SchoolID(self,req,schools_pk=None,pk=None):
        if(req.method == "PUT"):
        ################################ DESERIALIZER ################################
            student_data = JSONParser().parse(req)
            getStudent = Students.objects.get(id = pk,school = schools_pk)
            Student_serializer = StudentSerializer(student_data,data=getStudent)

        ################################ CHECK_OBJECT_VALID ################################
            if(Student_serializer.is_valid()):
                Student_serializer.save()
                return HttpResponse("Student updateddddddddd")
            else:
                print(Student_serializer.errors)
                return HttpResponse("update failed")
        elif(req.method == "PATCH"):
        ################################ DESERIALIZER ################################
            student_data = JSONParser().parse(req)
            getStudent = Students.objects.get(id = pk,school = schools_pk)
            Student_serializer = StudentSerializer(student_data,data=getStudent,partial=True)
            
        ################################ CHECK_OBJECT_VALID ################################
            if(Student_serializer.is_valid()):
                Student_serializer.save()
                return HttpResponse("Student updatedddddd")
            else:
                print(Student_serializer.errors)
                return HttpResponse("update failed")

    def DeleteStudentByID_AND_SchoolID(self,req,schools_pk=None,pk=None):
        getStudent = Students.objects.get(id = pk,school = schools_pk)
        getStudent.delete()
        return HttpResponse("delete student successfully")