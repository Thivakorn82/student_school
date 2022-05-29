"""n_squared_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import lookup
from email.mime import base
from django.contrib import admin
from django.urls import include, path
from Student_school import views
from rest_framework_nested import routers
from Student_school.views import GetOrCreateStudentsViewSet,GetOrEditByStudentsIDViewSet,GetOrPostSchoolViewSet,GetOrEditBySchoolIDViewSet,GetOrEditStudentByIDViewSet,GetOrPostStudentBySchoolIDViewSet

Students = GetOrCreateStudentsViewSet.as_view({
    'get': 'GetStudents',
    'post': 'PostStudent'
})

StudentsByID = GetOrEditByStudentsIDViewSet.as_view({
    'get': 'GetStudentByID',
    'put': 'UpdateStudent',
    'patch':'UpdateStudent',
    'delete':'DeleteStudent'
})

Schools = GetOrPostSchoolViewSet.as_view({
    'get': 'GetSchool',
    'post': 'PostSchool'
})

SchoolByID = GetOrEditBySchoolIDViewSet.as_view({
    'get':'GetSchoolByID',
    'put':'UpdateSchool',
    'patch':'UpdateSchool',
    'delete':'DeleteSchool'
})

StudentBySchoolID = GetOrPostStudentBySchoolIDViewSet.as_view({
    'get':'GetStudentBySchoolID',
    'post':'PostStudentBySchoolID'
})

StudentByBothID = GetOrEditStudentByIDViewSet.as_view({
    'get':'GetStudentByID_And_SchoolID',
    'put':'UpdateStudentByID_AND_SchoolID',
    'patch':'UpdateStudentByID_AND_SchoolID',
    'delete':'DeleteStudentByID_AND_SchoolID'
})

router = routers.DefaultRouter()
router.register('schools', GetOrPostSchoolViewSet,basename='schools')
# /schools/{pk}
school_router = routers.NestedSimpleRouter(router,r'schools',lookup='schools')
school_router.register('students', GetOrEditStudentByIDViewSet,basename='schools-students')
# /schools/{schools_pk}/students/{pk}

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'schools/', Schools),
    path(r'schools/<str:id>', SchoolByID),
    path(r'students/', Students),
    path(r'students/<str:id>/', StudentsByID),
    path(r'schools/<str:id>/students/', StudentBySchoolID),
    path('', include(school_router.urls))
]
