from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.forms.models import model_to_dict  # Import model_to_dict
# Create your models here.

#Teachers will be a custom user connected with django's built in User models
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(default=date.today)
    appt_date = models.DateField(null=True, blank=True)  # Date of Appointment
    special_assignment = models.CharField(max_length=100, blank=True)  # Special Assignment
    department = models.CharField(max_length=50, blank=True)  # Department
    employee_id = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    RANK_CHOICES = [
    ('Teacher I', 'Teacher I'),
    ('Teacher II', 'Teacher II'),
    ('Teacher III', 'Teacher III'),
    ('Teacher IV', 'Teacher IV'),
    ('Teacher V', 'Teacher V'),
    ('Teacher VI', 'Teacher VI'),
    ('Teacher VII', 'Teacher VII'),
    ('Master Teacher I', 'Master Teacher I'),
    ('Master Teacher II', 'Master Teacher II'),
    ('Master Teacher III', 'Master Teacher III'),
    ('Master Teacher IV', 'Master Teacher IV'),
]
    rank = models.CharField(max_length=30, choices=RANK_CHOICES, default='None')
    history = HistoricalRecords()
    def __str__(self):
        return self.last_name + ' ' + self.first_name

class Gradelevel(models.Model):
    GRADE_CHOICES = [
        ('Grade 7', 'Grade 7'),
        ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'),
        ('Grade 10', 'Grade 10'),
        ('Grade 11', 'Grade 11'),
        ('Grade 12', 'Grade 12'),
        ('Transitioning', 'Transitioning'),
    ]
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, unique=True)

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

#Students Class ____________________________________________________________________________________
class Student(models.Model):
    LRN = models.CharField(primary_key=True, max_length=30)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    suffix_name = models.CharField(max_length=10, blank=True, null=True)  # "Jr., I, II, III, etc.
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('For Dropout', 'For Dropout'),
        ('For Promotion', 'For Promotion'),
        ('For Retention', 'For Retention'),
        ('For Graduation', 'For Graduation'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, blank=True, null=True)

    birthday = models.DateField(default=date.today, null=True)
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
    religion = models.CharField(max_length=30, choices=RELIGION_CHOICES, default='other', null=True)
    other_religion = models.CharField(max_length=30, blank=True, null=True)  # This is finally working can now be added inside the information of the students
    age = models.IntegerField(null=True)
    semester = (
        ('Yearly', 'Yearly'),
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
    )
    sem = models.CharField(max_length=30, choices=semester, null=True, default='None')  ####
    classroom = models.ForeignKey('Classroom', null=True, verbose_name="Classrooms", on_delete=models.SET_NULL)
    gradelevel = models.ForeignKey('Gradelevel', on_delete=models.SET_NULL, null=True)
    sex_student = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = models.CharField(max_length=10, choices=sex_student, null=True)
    birth_place = models.CharField(max_length=20, null=True)
    mother_tongue = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)

    father_name = models.CharField(max_length=120, null=True)  # this section is for the parents and guardian
    father_contact = models.CharField(max_length=15, null=True)
    mother_name = models.CharField(max_length=120, null=True)  # this section is for the parents and guardian
    mother_contact = models.CharField(max_length=15, null=True)
    guardian_name = models.CharField(max_length=120, null=True)  # this section is for the parents and guardian
    guardian_contact = models.CharField(max_length=15, null=True)
    last_grade_level = models.IntegerField(null=True)  # this is for the returning learner
    last_school_attended = models.CharField(max_length=30, null=True)
    last_schoolyear_completed = models.CharField(max_length=12, null=True)
    academic_strand = (
        ('STEM', 'STEM'),
        ('BAM', 'BAM'),
        ('HESS', 'HESS'),
        ('SPORTS & ARTS', 'SPORTS & ARTS'),
        ('TVL', 'TVL'),
        ('GAS', 'GAS'),  # added for the strand
        ('HE', 'HE'),
        ('ICT', 'ICT'),
        ('IA', 'IA'),
        ('Not Applicable (JHS)', 'Not Applicable (JHS)'),
    )
    strand = models.CharField(choices=academic_strand, max_length=50, null=True)
    household_income_choices = (
        ('above Php 35,000', 'above Php 35,000'),
        ('from Php 18,000 - Php 35,000', 'from Php 18,000 - Php 35,000'),
        ('from Php 9,000 - Php 18,000', 'from Php 9,000 - Php 18,000'),
        ('below Php 9,000', 'below Php 9,000'),
    )
    household_income = models.CharField(max_length=30, choices=household_income_choices, null=True)
    is_returnee_student = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    is_returnee = models.CharField(max_length=5, choices=is_returnee_student, null=True)  ####
    drop_out = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    is_a_dropout = models.CharField(max_length=5, choices=drop_out, null=True)  #####
    working_student = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    is_a_working_student = models.CharField(max_length=5, choices=working_student, null=True)  ######
    previous_adviser = models.CharField(max_length=50, null=True)
    adviser_contact = models.IntegerField(null=True)
    health_bmi = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    general_average = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    scholarship_program = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    is_a_four_ps_scholar = models.CharField(max_length=5, choices=scholarship_program, null=True)  # 4ps scholarship program ##########
    history = HistoricalRecords()
    edited_fields = models.CharField(max_length=255, blank=True, null=True)  # Field to store edited fields
    notes = models.CharField(max_length=300, blank=True, null=True)

  
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