"""mysystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from data import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('user/', views.user_page, name='user_page'),


    #year of students
    path('grade_sections/', views.grade_sections, name='grade_sections'),
    path('classroom/<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('classrooms/add/', views.add_classroom, name='add_classroom'), # this is for adding a classroom
    path('classrooms/edit/<int:classroom_id>/', views.edit_classroom, name='edit_classroom'), #this for editing the classroom
    path('classroom/delete/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'), #this is for deleting classrooms
    
    
    path('students/', views.students_page, name='students'),
    
    path('teachers/', views.teachers_page, name='teachers'),
    path('edit_teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),

    path('<int:id>', views.students_page, name='view_student'), #view specific details of student
    
    path('create/', views.add_student, name='add_student'),  # for adding a student in the records
    path('delete/<int:id>/', views.destroy, name='delete_student'),  # for deleting a student
    path('update/<int:id>/', views.update, name='update_student'),  # for updating the editing of a student
    path('edit/<int:id>/', views.edit, name='edit_student'),  # for editing a student

    
    path('add/', views.add_teacher, name='add_teacher'),
    
     # this for the data visualization and analysis page 
    path('report/', views.report_page, name='report_page'),
   
    path('report_page/<int:classroom_id>/', views.report_page, name='report_page'),

    #STUDENT RECORD
    path('student_record/', views.student_record, name='student_record'),


]
