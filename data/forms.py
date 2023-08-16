from django import forms  
from django.forms import fields
from data.models import Student, Teacher, Classroom
from django.contrib.auth.models import User, Group
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        
        if self.instance.birthday: # this will automatically calculate the age of the student when the new year comes 
            today = date.today()
            next_birthday = self.instance.birthday.replace(year=today.year + 1)
            age = next_birthday.year - self.instance.birthday.year
            
            if today < next_birthday:
                age -= 1
            
            self.fields['age'] = forms.IntegerField(initial=age, disabled=True)



        if teacher and not is_admin:
            # Limit the choices for the classroom field to the classrooms of the teacher
            self.fields['classroom'].queryset = Classroom.objects.filter(teacher=teacher)
            # Set the default value for the classroom field to the teacher's classroom
            self.fields['classroom'].initial = Classroom.objects.filter(teacher=teacher)


    class Meta:
        model = Student
        fields = '__all__'

class AdminTeacherStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        
        if self.instance.birthday:
            today = date.today()
            age = today.year - self.instance.birthday.year
            if today.month < self.instance.birthday.month or (today.month == self.instance.birthday.month and today.day < self.instance.birthday.day):
                age -= 1
            self.fields['age'] = forms.IntegerField(initial=age, disabled=True)
        
        if teacher and is_admin:
            # Include all classrooms in the queryset
            self.fields['classroom'].queryset = Classroom.objects.all()
            # Set the default value for the classroom field to the teacher's classroom
            self.fields['classroom'].initial = teacher.classroom

    class Meta:
        model = Student
        fields = '__all__'
        
class TeacherSignupForm(UserCreationForm):
    birthday = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=True)
    tid = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    middle_name = forms.CharField(max_length=30, required=False)
    rank = forms.IntegerField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','middle_name', 'username', 'password1', 'password2', 'birthday')

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            teacher_group = Group.objects.get(name='TEACHER')
            user.groups.add(teacher_group)

            Teacher.objects.create(
                user=user,
                birthday=self.cleaned_data['birthday'],
                tid=self.cleaned_data['tid'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                rank=self.cleaned_data['rank']
            )
        
        return user


        
class TeacherForm(forms.ModelForm):
    # Additional fields for username, password, and group
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    group = forms.ChoiceField(choices=((1, 'TEACHER'), (2, 'ADMIN'), (3, 'BOTH TEACHER AND ADMIN')), required=True)

    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value for the username field
        self.fields['username'].initial = self.instance.user.username
        # Set initial value for the group field
        groups = self.instance.user.groups.all()
        if groups.filter(name='TEACHER').exists() and groups.filter(name='ADMIN').exists():
            self.fields['group'].initial = '3'  # BOTH TEACHER AND ADMIN
        elif groups.filter(name='TEACHER').exists():
            self.fields['group'].initial = '1'  # TEACHER
        elif groups.filter(name='ADMIN').exists():
            self.fields['group'].initial = '2'  # ADMIN

    def save(self, commit=True):
        # Save the teacher model
        teacher = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        group_choice = int(self.cleaned_data['group'])

        # Update the associated user model
        user = teacher.user
        user.username = username
        user.first_name = teacher.first_name  # Update the first name
        user.last_name = teacher.last_name  # Update the last name
        if password:
            user.set_password(password)
        if commit:
            teacher.save()
            user.save()
            # Update the group of the associated user
            teacher_group = Group.objects.get(name='TEACHER')
            admin_group = Group.objects.get(name='ADMIN')

            if group_choice == 1:  # TEACHER
                user.groups.set([teacher_group])
            elif group_choice == 2:  # ADMIN
                user.groups.set([admin_group])
            elif group_choice == 3:  # BOTH TEACHER AND ADMIN
                user.groups.set([teacher_group, admin_group])

        return teacher
        


#class StudentSearchForm(forms.Form):
 #   query = forms.IntegerField(label='LRN', required=True)
    
class StudentSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    
class TeacherSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)