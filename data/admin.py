from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . models import Student, Teacher, Classroom, Gradelevel
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False #Teacher should not be deletable unless the user is deleted first
    verbose_name_plural = 'Teachers'

class CustomizedUserAdmin(UserAdmin):
    inlines = (TeacherInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)


admin.site.register(Classroom)

class StudentMultiAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = (
        'LRN', 'last_name', 'first_name', 'middle_name', 'suffix_name', 'status',
        'birthday', 'religion', 'other_religion', 'age', 'sem', 'classroom',
        'gradelevel', 'sex', 'birth_place', 'mother_tongue', 'address',
        'father_name', 'father_contact', 'mother_name', 'mother_contact',
        'guardian_name', 'guardian_contact', 'strand', 'household_income',
        'is_returnee', 'is_a_dropout', 'is_a_working_student', 'health_bmi',
        'general_average', 'is_a_four_ps_scholar', 'edited_fields', 'notes',
        'g7_school', 'g7_schoolYear', 'g7_adviser', 'g7_adviserContact',
        'g8_school', 'g8_schoolYear', 'g8_adviser', 'g8_adviserContact',
        'g9_school', 'g9_schoolYear', 'g9_adviser', 'g9_adviserContact',
        'g10_school', 'g10_schoolYear', 'g10_adviser', 'g10_adviserContact',
        'g11_school', 'g11_schoolYear', 'g11_adviser', 'g11_adviserContact',
        'g12_school', 'g12_schoolYear', 'g12_adviser', 'g12_adviserContact', 
    )


admin.site.register(Student, StudentMultiAdmin)
admin.site.register(Gradelevel)

admin.site.register(Teacher, SimpleHistoryAdmin, inherit = True)