
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tablib import Dataset
from data.resources import ClassroomResource, StudentResource
from .forms import StudentForm
from .forms import TeacherForm
from .models import Student, Classroom, Teacher, Gradelevel
from django.db.models import Count
from django.views.generic import TemplateView # this is needed for the charts and graphs
from data.models import Student
import plotly.graph_objs as go
import plotly.io as pio
from .forms import StudentSearchForm, StudentForm, TeacherSearchForm, TeacherSignupForm, AdminTeacherStudentForm  # this is for the search function
import pandas as pd # this is for the data analysis
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.views.decorators.cache import cache_page #
from chartjs.views.lines import BaseLineChartView 
from django.http import HttpResponse
from django.db.models import Q
from .decorators import unauthenticated_user, allowed_users, admin_only
import random
import plotly.express as px
import datetime
import plotly.graph_objects as go
import logging
from django.forms.models import model_to_dict
# Create your views here.

@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        teacher_form = TeacherSignupForm(request.POST)
        if teacher_form.is_valid():
            user = teacher_form.save()
            
            messages.success(request, "User registration was successful!")

            print("User saved:", user)  # Print debug statement
            return redirect('login')
    else:
        teacher_form = TeacherSignupForm()
    return render(request, 'registration/signup.html', {
        'teacher_form': teacher_form
    })

#OG Login, signup pages
@login_required(login_url='login')
@admin_only
def home(request):
    count = User.objects.count()

    # Calculate male and female student counts
    male_count = Student.objects.filter(Q(sex='M') | Q(sex='Male')).count()
    female_count = Student.objects.filter(Q(sex='F') | Q(sex='Female')).count()

    # Calculate total student count
    total_students = male_count + female_count

    # Create pie chart data for gender distribution
    gender_labels = ['Male', 'Female']
    gender_values = [male_count, female_count]
    gender_colors = ['#1f77b4', '#ff7f0e'] # blue and orange colors for male and female respectively
    gender_trace = go.Pie(labels=gender_labels, values=gender_values, 
                          marker=dict(colors=gender_colors))
    gender_layout = go.Layout(title='Student Gender Distribution')
    gender_fig = go.Figure(data=[gender_trace], layout=gender_layout)
    gender_chart_div = pio.to_html(gender_fig, full_html=False)

    # Create bar chart data for scholarship program
    scholarship_labels = ['Yes', 'No']
    scholarship_counts = [
        Student.objects.filter(is_a_four_ps_scholar='1').count(),
        Student.objects.filter(is_a_four_ps_scholar='0').count()
    ]
    scholarship_colors = ['#2ca02c', '#d62728'] # green and red colors for Yes and No respectively
    scholarship_trace = go.Bar(x=scholarship_labels, y=scholarship_counts,
                               marker=dict(color=scholarship_colors))
    scholarship_layout = go.Layout(title='Student Scholarship Program')
    scholarship_fig = go.Figure(data=[scholarship_trace], layout=scholarship_layout)
    scholarship_chart_div = pio.to_html(scholarship_fig, full_html=False)

    # Create pie chart data for returnee status
    returnee_labels = ['Yes', 'No']
    returnee_values = [
        Student.objects.filter(is_returnee='1').count(),
        Student.objects.filter(is_returnee='0').count()
    ]
    returnee_colors = ['#9467bd', '#8c564b'] # purple and brown colors for Yes and No respectively
    returnee_trace = go.Pie(labels=returnee_labels, values=returnee_values, 
                             marker=dict(colors=returnee_colors))
    returnee_layout = go.Layout(title='Student Returnee Status')
    returnee_fig = go.Figure(data=[returnee_trace], layout=returnee_layout)
    returnee_chart_div = pio.to_html(returnee_fig, full_html=False)

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Retrieve total teachers and classrooms
    total_teachers = Teacher.objects.count()
    total_classrooms = Classroom.objects.count()

    # Add variables to context dictionary
    context = {
        'total_students': total_students,
        'gender_chart_div': gender_chart_div,
        'scholarship_chart_div': scholarship_chart_div,
        'returnee_chart_div': returnee_chart_div,
        'current_datetime': current_datetime,
        'count': count,
        'total_teachers': total_teachers,
        'total_classrooms': total_classrooms,
    }
    # Debug statement to print total students
    print("Debug Statement: Total Students -", total_students)
    print("Debug Statement: Total Students -", total_teachers)
    print("Debug Statement: Total Students -", total_classrooms)
    
    # Render the home.html template with the context data
    return render(request, 'home.html', context)


################################################## for class organization

@login_required
@allowed_users(allowed_roles=['ADMIN', 'TEACHER'])
def grade_sections(request):
    classrooms = Classroom.objects.order_by('gradelevel')
    tags = [
        {'gradelevel': 'Grade 7', 'classroom': classrooms.filter(gradelevel__grade='Grade 7')},
        {'gradelevel': 'Grade 8', 'classroom': classrooms.filter(gradelevel__grade='Grade 8')},
        {'gradelevel': 'Grade 9', 'classroom': classrooms.filter(gradelevel__grade='Grade 9')},
        {'gradelevel': 'Grade 10', 'classroom': classrooms.filter(gradelevel__grade='Grade 10')},
        {'gradelevel': 'Grade 11', 'classroom': classrooms.filter(gradelevel__grade='Grade 11')},
        {'gradelevel': 'Grade 12', 'classroom': classrooms.filter(gradelevel__grade='Grade 12')},
    ]
    context = {
         'tags':tags
         }

    return render(request, 'grade_sections.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['TEACHER'])
def user_page(request):
    # Retrieve all classrooms associated with the teacher
    classrooms = request.user.teacher.classroom_set.all()
    
    if classrooms.exists():
        # If at least one classroom exists
        classroom = classrooms[0]  # Get the first classroom
        students = Student.objects.filter(classroom=classroom)  # Filter students based on the classroom
    else:
        # If no classrooms exist
        classroom = None  # Set classroom to None
        students = []  # Set students as an empty list

    context = {'classroom': classroom, 'students': students}  # Prepare the context for rendering the template
    return render(request, 'user_page.html', context)  # Render the template with the context

@login_required
def classroom_detail(request, classroom_id): # this is for the individual classrooms selected which will bring the user to the class list
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    students = Student.objects.filter(classroom=classroom).order_by('last_name', 'first_name')
    context = {'classroom': classroom, 'students': students}
    
    return render(request, 'classroom_detail.html', context)
    

#####################################################################
@login_required
@admin_only
def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    user = teacher.user

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        username = request.POST.get('username', '')

        if form.is_valid() and not User.objects.filter(username=username).exclude(pk=user.pk).exists():
            user.username = username
            user.save()
            form.save()
            return redirect('teachers')
        else:
            messages.error(request, "Username already exists or form is invalid.")
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'edit_teacher.html', {'form': form, 'teacher_id': teacher_id, 'username': user.username})

@login_required
def students_page(request):
        student_list = Student.objects.all()
        return render(request,"view_students.html",{"students":student_list}) # this is to show the objects in the database


################################################################################ The CRUD Functions 
@login_required
def add_student(request):
    user = request.user

    if user.groups.filter(name='TEACHER').exists():
        teacher = user.teacher
        is_admin = user.groups.filter(name='ADMIN').exists()

        if request.method == 'POST':
            form = StudentForm(request.POST, teacher=teacher, is_admin=is_admin)
            if form.is_valid():
                form.save()
                print(f"Student added: {form.instance}")  # Print the saved student instance
                messages.success(request, "Student Added Successfully") # Notify user of successful Creation of student
                return redirect("user_page")
        else:
            form = StudentForm(teacher=teacher, is_admin=is_admin)
            form.fields['classroom'].queryset = Classroom.objects.filter(teacher=teacher)

    elif user.groups.filter(name='ADMIN').exists():
        if request.method == 'POST':
            form = AdminTeacherStudentForm(request.POST)
            if form.is_valid():
                form.save()
                print(f"Student added: {form.instance}")  # Print the saved student instance
                messages.success(request, "Student Added Successfully") # Notify user of successful Creation of student
                return redirect("students")
        else:
            form = StudentForm()
    else:
        # Handle other user groups or unauthorized access as desired
        return HttpResponse("Unauthorized access")

    context = {'form': form}
    return render(request, 'add_student.html', context)



@login_required
def destroy(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.error(request, "Student Deleted", extra_tags='danger')  # Set extra_tags to 'danger' for red color
    
    # Check if user belongs to the "TEACHER" group
    if request.user.groups.filter(name='TEACHER').exists():
        # Redirect to "user_page" if user is a teacher
        return redirect("user_page")
    else:
        # Redirect to "students" if user is not a teacher
        return redirect("students")

@login_required
def edit(request, lrn):
    student = get_object_or_404(Student, LRN=lrn)
    initial_data = model_to_dict(student)  # Store initial data for comparison
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            edited_fields = []  # Create a list to store edited fields and their previous values

            # Compare the new data with the initial data to detect edits
            for field_name, new_value in form.cleaned_data.items():
                if initial_data[field_name] != new_value:
                    previous_value = initial_data[field_name]
                    field_verbose_name = Student._meta.get_field(field_name).verbose_name
                    edited_fields.append(f"{field_verbose_name} (before: {previous_value})")

            # Store edited fields in the student object
            student.edited_fields = ', '.join(edited_fields)
            student.save()

            form.save()
            messages.success(request, "Student Updated Successfully")

            if request.user.groups.filter(name='TEACHER').exists():
                return redirect("user_page")
            else:
                return redirect("students")
    else:
        # Create the form instance without providing initial values
        form = StudentForm(instance=student)

        # Manually set the initial value for the 'sex' field
        form.fields['sex'].initial = student.sex
    context = {'form': form, 'student': student}
    return render(request, 'edit.html', context)




@login_required(login_url='login')
def update(request, id):
    student = Student.objects.get(id=id)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            print("Debug Statement: Student Updated -", student.name)  # Debug statement
            messages.success(request, "Student Updated Successfully") # Notify user of successful UPDATES of student
            return redirect("students")
    context = {'form': form, 'student': student}
    return render(request, 'update.html', context)



#######################################################################################

# this is the search function
@login_required(login_url='login')
def students_page(request):
    form = StudentSearchForm(request.GET or None)
    students = Student.objects.all().order_by('last_name', 'first_name')

    if form.is_valid():
        query = form.cleaned_data['query']
        students = students.filter(
            Q(LRN__icontains=query) |
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(suffix_name__icontains=query) |
            Q(classroom__classroom__icontains=query)   # Filter based on the 'classroom' field in the Classroom model
        ).order_by('last_name', 'first_name')
        print("Debug Statement: Searched Student -", query)  # Debug statement
        
    return render(request, 'view_students.html', {'form': form, 'students': students})

@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def teachers_page(request):
    form = TeacherSearchForm(request.GET or None)
    teachers = Teacher.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        teachers = teachers.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query)
        )
        print("Debug Statement: Searched Teacher -", query)  # Debug statement
        
    context = {'form': form, 'teachers': teachers}
    return render(request, 'view_teachers.html', context)




#################################### this to show the teachers data on the teachers page
#@login_required
#def teachers_page(request):
 #   teachers = Teacher.objects.all()
  #  context = {'teachers': teachers}
   # return render(request, 'view_teachers.html', context)

@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers_page')
    else:
        form = TeacherForm()
    context = {'form': form}
    return render(request, 'add_teacher.html', context)

################## This is for the report page

@login_required
def report_page(request):
    #selected_classroom = request.GET.get('classroom') # to show which classroom was selected
    # Use the selected_classroom value to filter or display the appropriate data in your report
    scholarship_labels = []  # Initialize the variable with an empty list
    scholarship_sizes = []  #Initialize scholarship_sizes with an empty list
    scholarship_title = ''  # Initialize scholarship_title with an empty string or an appropriate default value
    # Retrieve the list of classrooms
    #classrooms = Classroom.objects.all()

    # Retrieve selected classroom ID from the request
# Retrieve selected classroom ID from the request

    selected_gradelevel = request.GET.get('gradelevel')  # to show which grade level was selected
    print("Debug Statement: Selected Grade Level -", selected_gradelevel)  # Debug statement
    # Use the selected_gradelevel value to filter or display the appropriate data in your report
    
    # Retrieve the list of grade levels
    gradelevels = Gradelevel.objects.all()
    
    gradelevel_id = request.GET.get('gradelevel')

    # Retrieve selected grade level from the request
    if selected_gradelevel == "all":
        # Retrieve all students since "all" grade levels were selected
        students = Student.objects.all()
    elif selected_gradelevel:
        # Retrieve data from the database based on the selected grade level
        students = Student.objects.filter(gradelevel_id=selected_gradelevel)
    else:
        # If no grade level is provided, retrieve all students
        students = Student.objects.all()

    # Calculate strand distribution
    strand_counts = dict()
    for student in students:
        strand = student.strand
        strand_counts[strand] = strand_counts.get(strand, 0) + 1

    # Prepare data for strand bar chart
    strand_labels = [strand[1] for strand in Student.academic_strand]
    strand_sizes = [strand_counts.get(strand[0], 0) for strand in Student.academic_strand]
    strand_title = 'Distribution of Academic Strands'

    # Calculate economic status distribution
    economic_counts = dict()
    for student in students:
        economic = student.household_income
        economic_counts[economic] = economic_counts.get(economic, 0) + 1

    # Prepare data for economic status bar chart
    economic_labels = [choice[1] for choice in Student.household_income_choices]
    economic_sizes = [economic_counts.get(choice[0], 0) for choice in Student.household_income_choices]
    economic_title = 'Distribution of household income'
    # Calculate religion distribution
    religion_counts = dict()
    for student in students:
        religion = student.religion
        religion_counts[religion] = religion_counts.get(religion, 0) + 1

    # Prepare data for religion bar chart
    religion_labels = [religion[1] for religion in Student.RELIGION_CHOICES]
    religion_sizes = [religion_counts.get(religion[0], 0) for religion in Student.RELIGION_CHOICES]
    religion_title = 'Distribution of Religions'

    # Calculate dropout distribution
    dropout_counts = dict()
    for student in students:
        dropout = student.is_a_dropout
        dropout_counts[dropout] = dropout_counts.get(dropout, 0) + 1

    # Prepare data for dropout pie chart
    dropout_labels = [dropout[1] for dropout in Student.drop_out]
    dropout_sizes = [dropout_counts.get(dropout[0], 0) for dropout in Student.drop_out]
    dropout_title = 'Distribution of Dropout Status'

    # Calculate working student distribution
    working_student_counts = dict()
    for student in students:
        working_student = student.is_a_working_student
        working_student_counts[working_student] = working_student_counts.get(working_student, 0) + 1

    # Prepare data for working student pie chart
    working_student_labels = [working_student[1] for working_student in Student.working_student]
    working_student_sizes = [working_student_counts.get(working_student[0], 0) for working_student in Student.working_student]
    working_student_title = 'Distribution of Working Students'

    # Calculate scholarship program distribution
    scholarship_counts = dict()
    for student in students:
        scholarship = student.is_a_four_ps_scholar
        scholarship_counts[scholarship] = scholarship_counts.get(scholarship, 0) + 1

    # Prepare data for scholarship program pie chart
        scholarship_labels = [scholarship[1] for scholarship in Student.scholarship_program]
        scholarship_sizes = [scholarship_counts.get(scholarship[0], 0) for scholarship in Student.scholarship_program]
        scholarship_title = 'Distribution of Scholarship Programs'

    # Calculate sex distribution
    sex_counts = dict()
    for student in students:
        sex = student.sex
        sex_counts[sex] = sex_counts.get(sex, 0) + 1

    # Prepare data for sex pie chart
    sex_labels = [sex[1] for sex in Student.sex_student]
    sex_sizes = [sex_counts.get(sex[0], 0) for sex in Student.sex_student]
    sex_title = 'Distribution of Sex'

    # Calculate returnee student distribution
    returnee_counts = dict()
    for student in students:
        returnee = student.is_returnee
        returnee_counts[returnee] = returnee_counts.get(returnee, 0) + 1

    # Prepare data for returnee student pie chart
    returnee_labels = [returnee[1] for returnee in Student.is_returnee_student]
    returnee_sizes = [returnee_counts.get(returnee[0], 0) for returnee in Student.is_returnee_student]
    returnee_title = 'Distribution of Returnee Students'

    # Create and save pie chart figures
    #strand_fig = create_pie_chart(strand_labels, strand_sizes, strand_title)
    #economic_fig = create_pie_chart(economic_labels, economic_sizes, economic_title)
    dropout_fig = create_pie_chart(dropout_labels, dropout_sizes, dropout_title)
    working_student_fig = create_pie_chart(working_student_labels, working_student_sizes, working_student_title)
    scholarship_fig = create_pie_chart(scholarship_labels, scholarship_sizes, scholarship_title)
    sex_fig = create_pie_chart(sex_labels, sex_sizes, sex_title)
    returnee_fig = create_pie_chart(returnee_labels, returnee_sizes, returnee_title)

    # Create and save bar chart figures with bright colors
    #modality_fig = create_bar_chart(modality_labels, modality_sizes, modality_title, colorscale='bright')
    religion_fig = create_bar_chart(religion_labels, religion_sizes, religion_title, colorscale='bright')
    strand_fig = create_bar_chart(strand_labels, strand_sizes, strand_title, colorscale='bright')
    economic_fig = create_bar_chart(economic_labels, economic_sizes, economic_title, colorscale='bright')
    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render(request, 'report_page.html', {
        'current_datetime': current_datetime,
        'strand_chart': strand_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        #'modality_chart': modality_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'economic_chart': economic_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'religion_chart': religion_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'dropout_chart': dropout_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'working_student_chart': working_student_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'scholarship_chart': scholarship_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'sex_chart': sex_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        'returnee_chart': returnee_fig.to_html(full_html=False, include_plotlyjs='cdn'),
        #'classrooms': classrooms,  # Pass the classrooms variable
        #'selected_classroom': selected_classroom, #passed the selected classroom variable
        'gradelevels': gradelevels,  # Pass the gradelevels variable
        'selected_gradelevel': selected_gradelevel,  # Passed the selected grade level variable

    })

def create_pie_chart(labels, sizes, title):
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig.update_layout(title=title)
    return fig

def create_bar_chart(labels, sizes, title, colorscale='bright'):
    colors = px.colors.qualitative.Plotly
    fig = go.Figure(data=[go.Bar(x=labels, y=sizes, marker_color=colors)])
    fig.update_layout(title=title)
    return fig

############################### this is for adding classrooms and assigning a teacher to those classrooms
def add_classroom(request):
    if request.method == 'POST':
        # Retrieve the values from the form
        classroom_name = request.POST.get('classroom_name')
        gradelevel_id = request.POST.get('gradelevel_id')
        teacher_id = request.POST.get('teacher_id')

        try:
            # Attempt to retrieve the Gradelevel object with the given ID
            gradelevel = Gradelevel.objects.get(id=gradelevel_id)

            if teacher_id:  # Check if a teacher is selected
                # Retrieve the Teacher object with the given ID
                teacher = Teacher.objects.get(id=teacher_id)
            else:
                teacher = None  # Set teacher to None if no teacher is selected

            # Create a new Classroom object with the provided values
            Classroom.objects.create(classroom=classroom_name, gradelevel=gradelevel, teacher=teacher)
            
            # Debug print statements
            print("Debug Statement: Classroom added")
            print("Classroom name:", classroom_name)
            print("Teacher:", teacher)
            print("Grade level:", gradelevel)
            
            return redirect('grade_sections')
        except Gradelevel.DoesNotExist:
            print("Gradelevel does not exist")  # Debug statement
            # Handle the error or redirect to an appropriate page
        except Teacher.DoesNotExist:
            print("Teacher does not exist")  # Debug statement
            # Handle the error or redirect to an appropriate page

    # Retrieve all the available grade levels and teachers
    gradelevels = Gradelevel.objects.all()
    teachers = Teacher.objects.all()

    
    
    # Render the template with the grade levels and teachers
    return render(request, 'add_classroom.html', {'gradelevels': gradelevels, 'teachers': teachers})



############################### this is for editting the classrooms and their assigned teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def edit_classroom(request, classroom_id):
    try:
        # Retrieve the classroom object based on the provided classroom_id
        classroom = Classroom.objects.get(id=classroom_id)
    except Classroom.DoesNotExist:
        # Handle the case where the classroom doesn't exist
        return HttpResponse("Classroom does not exist.")

    if request.method == 'POST':
        # Retrieve the form data submitted via POST
        classroom_name = request.POST.get('classroom_name')
        gradelevel_id = request.POST.get('gradelevel_id')
        teacher_id = request.POST.get('teacher_id')

        try:
            # Retrieve the gradelevel object based on the selected gradelevel_id
            gradelevel = Gradelevel.objects.get(id=gradelevel_id)
        except Gradelevel.DoesNotExist:
            # Handle the case where the grade level doesn't exist
            return HttpResponse("Grade level does not exist.")

        if teacher_id == "-1":
            # If the selected teacher_id is -1 (None), set the teacher to None
            teacher = None
        else:
            try:
                # Retrieve the teacher object based on the selected teacher_id
                teacher = Teacher.objects.get(id=teacher_id)
            except Teacher.DoesNotExist:
                # Handle the case where the teacher doesn't exist
                return HttpResponse("Teacher does not exist.")

        # Update the classroom object with the new data
        classroom.classroom = classroom_name
        classroom.gradelevel = gradelevel
        classroom.teacher = teacher
        classroom.save()

        # Redirect to the appropriate page after saving
        return redirect('grade_sections')

    # Retrieve all gradelevels and teachers for rendering the form
    gradelevels = Gradelevel.objects.all()
    teachers = Teacher.objects.all()

    # Prepare the context to pass to the template
    context = {
        'classroom': classroom,
        'gradelevels': gradelevels,
        'teachers': teachers,
        'current_gradelevel': classroom.gradelevel.id
    }

    print("Debug Statement: Edited Classroom")
    print("Classroom name:", classroom.classroom)
    print("Teacher:", classroom.teacher)
    print("Grade level:", classroom.gradelevel)

    # Render the edit_classroom.html template with the provided context
    return render(request, 'edit_classroom.html', context)




############################### this is for deleting classrooms
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    if request.method == 'POST':
        print("Debug Statement: Deleting Classroom -", classroom.classroom)  # Debug statement
        classroom.delete()
        
        teachers = Teacher.objects.all()  # Add this line to retrieve all teachers
    return redirect('grade_sections')

########################### STUDENT RECORD
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def student_record(request):
    # Get the desired fields from the StudentRecord model
    #student_records = StudentRecord.objects.values('LRN', 'last_name', 'first_name', 'gradelevel__grade_level', 'classroom__section')
    student_records = Student.history.all()
    
    context = {'student_records': student_records}
    return render(request, 'student_record.html', context)

@allowed_users(allowed_roles=['ADMIN'])
def export_students_to_excel(request):
    students = Student.objects.all()

    # Create a DataFrame with fields from the Student model and related data
    data = {
        'LRN': [student.LRN for student in students],
        'last_name': [student.last_name for student in students],
        'first_name': [student.first_name for student in students],
        'middle_name': [student.middle_name for student in students],
        'suffix_name': [student.suffix_name for student in students],
        'status': [student.status for student in students],
        'birthday': [student.birthday.strftime('%d/%m/%Y') if student.birthday else None for student in students],
        'religion': [student.religion for student in students],
        'other_religion': [student.other_religion for student in students],
        'age': [student.age for student in students],
        'sem': [student.sem for student in students],
        'classroom': [student.classroom.classroom if student.classroom else None for student in students],
        'gradelevel': [student.gradelevel.grade if student.gradelevel else None for student in students],
        'sex': [student.sex for student in students],
        'birth_place': [student.birth_place for student in students],
        'mother_tongue': [student.mother_tongue for student in students],
        'address': [student.address for student in students],
        'father_name': [student.father_name for student in students],
        'father_contact': [student.father_contact for student in students],
        'mother_name': [student.mother_name for student in students],
        'mother_contact': [student.mother_contact for student in students],
        'guardian_name': [student.guardian_name for student in students],
        'guardian_contact': [student.guardian_contact for student in students],
        'last_grade_level': [student.last_grade_level for student in students],
        'last_school_attended': [student.last_school_attended for student in students],
        'last_schoolyear_completed': [student.last_schoolyear_completed for student in students],
        'strand': [student.strand for student in students],
        'household_income': [student.household_income for student in students],
        'is_returnee': [student.is_returnee for student in students],
        'is_a_dropout': [student.is_a_dropout for student in students],
        'is_a_working_student': [student.is_a_working_student for student in students],
        'previous_adviser': [student.previous_adviser for student in students],
        'adviser_contact': [student.adviser_contact for student in students],
        'health_bmi': [student.health_bmi for student in students],
        'general_average': [student.general_average for student in students],
        'is_a_four_ps_scholar': [student.is_a_four_ps_scholar for student in students],
        'notes': [student.notes for student in students],
    }

    df = pd.DataFrame(data)

    # Convert DataFrame to Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students_data.xlsx"'

    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False)

    return response

#EXPORT 
@allowed_users(allowed_roles=['ADMIN'])
def export_classrooms_to_excel(request):
    classrooms = Classroom.objects.all().values()
    df = pd.DataFrame(list(classrooms))

    # Convert DataFrame to Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="classrooms_data.xlsx"'

    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False)

    return response

#IMPORT
#This view function handles student data import from an Excel file.

def import_students_from_excel(request):
    # Processes the student import request.

    if request.method == 'POST':  # Check if a POST request (file submission) was made
        student_resource = StudentResource()  # Instantiate a StudentResource object (likely for data validation)
        dataset = Dataset()  # Instantiate a Dataset object for loading the Excel data
        new_student = request.FILES['myfile']  # Retrieve the uploaded file from the request

        if not new_student.name.endswith('xlsx'):  # Validate file extension
            messages.error(request, 'Please upload an Excel file only (.xlsx)')  # Display an error message
            return render(request, 'view_students.html')  # Re-render the view_students.html page

        try:
            imported_data = dataset.load(new_student.read(), format='xlsx')  # Load Excel data into a dataset
            successfully_imported = 0

            for data in imported_data:  # Iterate through each student record in the dataset
                classroom_identifier = data[12]  # Extract classroom identifier from the 13th column (index 12)
                gradelevel_identifier = data[13]  # Extract grade level identifier from the 14th column (index 13)
                print("Classroom Identifier:", classroom_identifier)  # Log classroom identifier
                classroom_instance = Classroom.objects.get(classroom=classroom_identifier)  # Retrieve classroom object
                gradelevel_instance = Gradelevel.objects.get(grade=gradelevel_identifier)

                try:
                    # Create a new Student object with data from the Excel row
                    value = Student(
                        LRN=data[1],
                        last_name=data[2],
                        first_name=data[3],
                        middle_name=data[4],
                        suffix_name=data[5],
                        status=data[6],
                        birthday=data[7],
                        religion=data[8],
                        other_religion=data[9],
                        age=data[10],
                        sem=data[11],
                        classroom=classroom_instance,  # Assign retrieved classroom object
                        gradelevel=gradelevel_instance,  # Assign retrieved grade level object
                        sex=data[14],
                        birth_place=data[15],
                        mother_tongue=data[16],
                        address=data[17],
                        father_name=data[18],
                        father_contact=data[19],
                        mother_name=data[20],
                        mother_contact=data[21],
                        guardian_name=data[22],
                        guardian_contact=data[23],
                        last_grade_level=data[24],
                        last_school_attended=data[25],
                        last_schoolyear_completed=data[26],
                        strand=data[27],
                        household_income=data[28],
                        is_returnee=data[29],
                        is_a_dropout=data[30],
                        is_a_working_student=data[31],
                        previous_adviser=data[32],
                        adviser_contact=data[33],
                        health_bmi=data[34],
                        general_average=data[35],
                        is_a_four_ps_scholar=data[36],
                        notes=data[37]
                    )
                    value.save()  # Save the student object to the database
                except Exception as e:
                    messages.error(request, f"Error saving student data: {str(e)}")

            if successfully_imported > 0:
                messages.success(request, f"Successfully imported {successfully_imported} student(s) into the database.")

        except Exception as e:
            messages.info(request, f"Error loading student/s from the file: {str(e)}")

    return render(request, 'view_students.html')  # Re-render the view_students.html page after processing
#===============================================================#

def import_classrooms_from_excel(request):
    # Processes the classroom import request.

    if request.method == 'POST':  # Check if a POST request (file submission) was made
        classroom_resource = ClassroomResource()  # Instantiate a ClassroomResource object (likely for data validation)
        dataset = Dataset()  # Instantiate a Dataset object for loading the Excel data
        new_classroom = request.FILES['myfile']  # Retrieve the uploaded file from the request

        if not new_classroom.name.endswith('xlsx'):  # Validate file extension
            messages.error(request, 'Please upload an Excel file only (.xlsx)')  # Display an error message
            return render(request, 'grade_sections.html')  # Re-render the view_classrooms.html page

        try:
            imported_data = dataset.load(new_classroom.read(), format='xlsx')  # Load Excel data into a dataset
            successfully_imported = 0

            for data in imported_data:  # Iterate through each classroom record in the dataset
                grade_level_identifier = data[0]  # Extract grade level identifier from the 1st column (index 0)
                grade_level_instance = Gradelevel.objects.get(grade=grade_level_identifier)  # Retrieve grade level object

                try:
                    # Create a new Classroom object with data from the Excel row
                    classroom = Classroom(
                        gradelevel=grade_level_instance,  # Assign retrieved grade level object
                        classroom=data[1],
                        teacher=None  # Replace None with actual teacher data if available
                    )
                    classroom.save()  # Save the classroom object to the database
                    successfully_imported += 1
                except Exception as e:
                    messages.error(request, f"Error saving classroom data: {str(e)}")

            if successfully_imported > 0:
                messages.success(request, f"Successfully imported {successfully_imported} classroom(s) into the database.")

        except Exception as e:
            messages.info(request, f"Error loading classroom/s from the file: {str(e)}")

    return render(request, 'grade_sections.html')  # Re-render the view_classrooms.html page after processing


#BULKPROMOTE

@login_required(login_url='login')
def students_for_promotion(request):
    # Get students for promotion
    students_grade_8 = Student.objects.filter(
        Q(status='For Promotion') | Q(status='For Retention'),
        gradelevel__grade='Grade 8',
    )

    # Add queries for other grade levels
    students_grade_9 = Student.objects.filter(
        Q(status='For Promotion') | Q(status='For Retention'),
        gradelevel__grade='Grade 9',
    )

    students_grade_10 = Student.objects.filter(
        Q(status='For Promotion') | Q(status='For Retention'),
        gradelevel__grade='Grade 10',
    )

    students_grade_11 = Student.objects.filter(
        Q(status='For Promotion') | Q(status='For Retention'),
        gradelevel__grade='Grade 11',
    )

    students_grade_12 = Student.objects.filter(
        Q(status='For Promotion') | Q(status='For Retention'),
        gradelevel__grade='Grade 12',
    )

    classrooms = Classroom.objects.all()

    # A dictionary to hold classrooms for each grade level

     # Assuming you have a predefined list of grade levels
    grade_levels = Gradelevel.objects.all()
    grade_level_classrooms = {grade.id: Classroom.objects.filter(gradelevel=grade) for grade in grade_levels}

    for grade, students in [('Grade 8', students_grade_8), ('Grade 9', students_grade_9), ('Grade 10', students_grade_10), ('Grade 11', students_grade_11), ('Grade 12', students_grade_12)]:  # and so on for each grade
        for student in students:
            student.classroom_options = grade_level_classrooms[student.gradelevel_id]
            student.LRN_str = str(student.LRN)  # Add LRN as a string to the context


    # Other necessary context data (if needed)
    context = {
        'students_grade_8': students_grade_8,
        'students_grade_9': students_grade_9,
        'students_grade_10': students_grade_10,
        'students_grade_11': students_grade_11,
        'students_grade_12': students_grade_12,
        'classrooms' : classrooms,
    }

    return render(request, 'students_for_promotion.html', context)

@login_required(login_url='login')
def assign_classroom_bulk(request, grade):
    if request.method == 'POST':
        # List to store student LRNs for updating status
        student_lrns = []

        for key, value in request.POST.items():
            if key.startswith('classroom_'):
                student_lrn_str = key.split('_')[1] 
                classroom_id = value

                try:
                    student = Student.objects.get(LRN=str(student_lrn_str))  # Convert LRN to string for comparison
                    classroom = Classroom.objects.get(id=classroom_id)
                    student.classroom = classroom
                    student.status = 'Processing'  # Update status to "Processing"
                    student.save()
                    student_lrns.append(student_lrn_str)  # Use LRN_str here

                except Student.DoesNotExist:
                    messages.warning(request, f"Student with LRN {student_lrn_str} does not exist. Skipping.")
                    continue

                except Classroom.DoesNotExist:
                    messages.warning(request, f"Classroom with ID {classroom_id} does not exist. Skipping.")
                    continue

        # Update status for all selected students
        Student.objects.filter(LRN__in=student_lrns).update(status='Processing')

        messages.success(request, 'Students assigned to classrooms successfully.')
        return redirect('students_for_promotion')  # Redirect back to the promotion page
    
@login_required(login_url='login')
def bulk_promote_students(request):
    if request.method == 'POST':
        try:
            # Assuming there is a direct reference from Classroom to Teacher
            user_classroom = Classroom.objects.get(teacher__user=request.user)
        except Classroom.DoesNotExist:
            # Handle the case where there is no associated Classroom for the teacher
            messages.error(request, 'User is not associated with a classroom.')
            return redirect('students')  # Replace 'students' with the actual URL name of your students page

        # Determine the next grade level based on the teacher's current grade level
        current_grade = user_classroom.gradelevel.grade
        next_grade = get_next_grade(current_grade)

        if next_grade is None:
            messages.error(request, 'Unable to determine the next grade level.')
            return redirect('students')  # Replace 'students' with the actual URL name of your students page

        next_grade_instance = Gradelevel.objects.get(grade=next_grade)

        students_to_promote = Student.objects.filter(
            classroom=user_classroom,
            # Add other conditions based on your model structure
            # For example, grade = 'Grade 7', 'Grade 8', 'Grade 10', 'Grade 11'
        )

        # Update each student's grade and status
        for student in students_to_promote:
            student.gradelevel = next_grade_instance
            student.status = 'For Promotion'
            student.classroom = Classroom.objects.get(classroom='FOR PROMOTION')  # Change to the actual name of the 'FOR PROMOTION' classroom
            student.save()

        messages.success(request, f'Bulk promotion to {next_grade} successful!')

    return redirect('user_page')  # Replace 'students' with the actual URL name of your students page


def get_next_grade(current_grade):
    # Define the grade progression logic here
    grade_sequence = ['Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']

    try:
        current_index = grade_sequence.index(current_grade)
        next_index = current_index + 1

        if next_index < len(grade_sequence):
            return grade_sequence[next_index]
        else:
            return None  # No next grade (end of sequence)
    except ValueError:
        return None  # Current grade not found in the sequence