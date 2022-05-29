from rest_framework import serializers
from Student_school.models import Students,Schools

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= Schools
        fields=('school_name','max_students')

class StudentSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=Schools.objects.all(),
                                                many=False)
    class Meta:
        model= Students
        fields=('student_firstname','student_lastname','school')