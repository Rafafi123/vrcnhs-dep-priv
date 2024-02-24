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
from django.contrib.auth import views as auth_views

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
    path('view_student_detail/<int:lrn>/', views.view_student_detail, name='view_student_detail'),
    
    path('teachers/', views.teachers_page, name='teachers'),
    #DELETE TEACHER
    path('delete_teacher/<int:teacher_id>/', views.destroy_teacher, name='delete_teacher'),

    path('returning', views.back_student_detail, name='back_student_detail'),

    path('edit_teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),

    path('<int:id>', views.students_page, name='view_student'), #view specific details of student
    
    path('create/', views.add_student, name='add_student'),  # for adding a student in the records
    path('delete/<int:lrn>/', views.destroy, name='delete_student'),  # for deleting a student
    path('update/<int:lrn>/', views.update, name='update_student'),  # for updating the editing of a student
    path('edit/<int:lrn>/', views.edit, name='edit_student'),  # for editing a student

    
    path('add/', views.add_teacher, name='add_teacher'),
    
     # this for the data visualization and analysis page 
    path('report/', views.report_page, name='report_page'),
   
    path('report_page/<int:classroom_id>/', views.report_page, name='report_page'),

    #STUDENT RECORD
    path('student_record/', views.student_record, name='student_record'),

    #Back button from register a student to view all students
    path('students/', views.students_page, name='students'),

    #import export
    path('export_students/', views.export_students_to_excel, name='export_students'),
    path('export/classrooms/', views.export_classrooms_to_excel, name='export_classrooms_to_excel'),

    path('download-template/', views.download_template, name='download_template'),
    path('import/', views.import_students_from_excel, name='import_students'),
    #path('import_user/', views.import_students_from_excel_USER, name='import_students_user'),
    path('import_classroom/', views.import_classrooms_from_excel, name='import_classrooms'),

    #Bulk Promote
    path('students_for_promotion/', views.students_for_promotion, name='students_for_promotion'),

    path('assign_classroom_bulk/<str:grade>/', views.assign_classroom_bulk, name='assign_classroom_bulk'),
    path('bulk_promote_students/', views.bulk_promote_students, name='bulk_promote_students'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)


    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_changed.html'), 
        name='password_change_done'),
]