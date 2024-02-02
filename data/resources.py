from import_export import resources
from .models import Student, Classroom

class StudentResource(resources.ModelResource):
    class meta:
        model = Student 

class ClassroomResource(resources.ModelResource):
    class meta:
        model = Classroom
        