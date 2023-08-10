from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# Create your models here.

#Teachers will be a custom user connected with django's built in User models
class Teacher(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   birthday = models.DateField(default=date.today)
   tid = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   first_name = models.CharField(max_length=30)
   middle_name = models.CharField(max_length=30)
   rank = models.IntegerField() # ranking of teachers
   history = HistoricalRecords() 
   def __str__(self):
    return self.last_name + ' ' + self.first_name

class Gradelevel(models.Model):
    grade = models.CharField(max_length=50)

    def __str__(self):
        return self.grade

class Classroom(models.Model):
    gradelevel = models.ForeignKey(Gradelevel,blank=True, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=50, null=True, default = None)
    teacher = models.ForeignKey(Teacher,blank=True, null=True, default = None, verbose_name =  "Teachers", on_delete=models.SET_DEFAULT)
   

    class Meta:
        verbose_name_plural = "Classrooms"   

    def __str__(self):
        return self.classroom


class Student(models.Model):
    LRN = models.PositiveIntegerField()
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    suffix_name = models.CharField(max_length=10, blank=True) # "Jr., I, II, III, etc. 
    birthday = models.DateField(default=date.today)
    RELIGION_CHOICES = [
        ('Christianity', 'Christianity'),
        ('Roman catholic', 'Roman Catholic'),
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Judaism', 'Judaism'),
        ('Sikhism', 'Sikhism'),
        ('Other', 'Other'),
    ]
    religion = models.CharField(max_length=30, choices=RELIGION_CHOICES, default='other')
    other_religion = models.CharField(max_length=30, blank=True)# This is finally working can now be added inside the information of the students
    age = models.IntegerField()
    semester =(
        (1, 'Yearly'),
        (2, '1st Semester'),
        (3, '2nd Semester'),
    )
    sem = models.IntegerField(choices=semester, null=True)####   
    classroom = models.ForeignKey(Classroom, default=1, verbose_name =  "Classrooms", on_delete=models.SET_DEFAULT)
    gradelevel = models.ForeignKey(Gradelevel, on_delete=models.SET_NULL, null=True)
    sex_student = (
    ('M', 'Male'),
    ('F', 'Female'),
    )
    sex = models.CharField(max_length=2, choices=sex_student)
    birth_place = models.CharField(max_length=20)
    mother_tongue = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    father_name = models.CharField(max_length=120) # this section is for the parents and guardian
    father_contact = models.IntegerField()
    mother_name = models.CharField(max_length=120) # this section is for the parents and guardian
    mother_contact = models.IntegerField()
    guardian_name = models.CharField(max_length=120) # this section is for the parents and guardian
    guardian_contact = models.IntegerField()
    last_grade_level = models.IntegerField() # this is for the returning learner
    last_school_attended = models.CharField(max_length=30)
    last_schoolyear_completed = models.CharField(max_length=4)
    academic_strand = (
    ('A', 'STEM'),
    ('B', 'BAM'),
    ('C', 'HESS'),
    ('D', 'SPORTS & ARTS'),
    ('E', 'TVL'),
    ('GAS', 'GAS'), #added for the strand
    ('HE', 'HE'),
    ('ICT', 'ICT'),
    ('IA', 'IA'),
    ('N/A', 'Not Applicable (JHS)'),
    )
    strand = models.CharField(choices=academic_strand, max_length=15)
    text = models.TextField(blank=True, null=True)
    economic_status = (
    ('A', 'Upper Class: above Php 35,000'),
    ('B', 'Middle Class: from Php 18,000 - Php 35,000'),
    ('C', 'Working Class: from Php 9000 - Php 18,000'),
    ('D', 'Lower Class: below Php 9000'),
    )
    economic_range = models.CharField(max_length=1, choices=economic_status)
    is_returnee_student = (
        ('1', 'Yes'),
        ('0', 'No')
    )
    is_returnee = models.CharField(max_length=1, choices=is_returnee_student)####
    drop_out = (
        ('1', 'Yes'),
        ('0', 'No')
    )
    is_a_dropout = models.CharField(max_length=1, choices=drop_out)#####
    working_student = (
        ('1', 'Yes'),
        ('0', 'No')
    )
    is_a_working_student = models.CharField(max_length=1, choices=working_student)######
    previous_adviser = models.CharField(max_length=50)
    adviser_contact = models.IntegerField()
    health_bmi =  models.DecimalField(max_digits=10, decimal_places=2)
    general_average = models.DecimalField(max_digits=10, decimal_places=2)
    scholarship_program = (
        ('1', 'Yes'),
        ('0', 'No')
    )
    is_a_four_ps_scholar = models.CharField(max_length=1, choices=scholarship_program) #4ps scholarship program ##########
    history = HistoricalRecords()
  
    class Meta:
        verbose_name_plural = "Students"   

    def save(self, *args, **kwargs):
        # Calculate the age by subtracting the birth year from the current year
        self.age = date.today().year - self.birthday.year

        # Call the save method of the parent class to save the object
        super().save(*args, **kwargs)
    def __str__(self):
	    return self.last_name + ' ' + self.first_name

 # The Meta class inside the student class is used to specify the name of the database table that will be used to store instances of the student model.
class Meta:  
    db_table = "student"  