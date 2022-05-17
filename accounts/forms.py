from college.models import Teacher, Student
from django import forms
from django.forms import ModelForm
from django.forms import ValidationError
from django.contrib.auth.models import User
class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Teacher
        fields = "__all__"
    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        print(username)
        try:
            user = User.objects.get(username = username)
            self.add_error('username', "Teacher with this Username already exists.")
        except Exception:
            pass    
        return username


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = ["username", "name", "prn", "branch", "email"]

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        print(username)
        try:
            user = User.objects.get(username = username)
            self.add_error('username', "Student with this Username already exists.")
        except Exception:
            pass    
        return username