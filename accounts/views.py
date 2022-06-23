from .forms import TeacherForm, StudentForm
from college.models import Branch, Student, Teacher
from college.helpers import apology
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMessage
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
# Create your views here.


class TeacherLogin(View):
    def get(self, request): 
        return render(request, "accounts/teacher_login.html")
    
    def post(self, request):
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            checked = Teacher.objects.values('username').get(username = username)
        except Exception:
            return apology(request, "Invalid UserName or Password!")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse_lazy("college:teacherview"))

        return apology(request, "Invalid UserName or Password!")


class StudentLogin(View):
    def get(self, request): 
        return render(request, "accounts/student_login.html")
    
    def post(self, request):
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            checked = Student.objects.values('username').get(username = username)
        except Exception:
            return apology(request, "Invalid UserName or Password!")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse_lazy("college:studentview"))

        return apology(request, "Invalid UserName or Password!")


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "accounts:loginadmin"
    def test_func(self):
        return self.request.user.is_superuser

class StudentLoginRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "accounts:loginstudent"
    def test_func(self):
        isStudent = False
        try:
            user = Student.objects.get(username = self.request.user)
            isStudent = True 
        except Exception:
            isStudent = False
        return isStudent


class TeacherLoginRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "accounts:loginteacher"
    def test_func(self):
        isTeacher = False
        try:
            user = Teacher.objects.get(username = self.request.user)
            isTeacher = True 
        except Exception:
            isTeacher = False
        return isTeacher
class RegisterTeacher(SuperUserRequiredMixin, CreateView):
    form_class = TeacherForm
    model = Teacher
    success_url = reverse_lazy("college:adminview")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.data.get("password")
        email = form.cleaned_data.get("email")
        # print(username)
        # print(password)
        try:
            User.objects.create_user(username = username, password = password)
        except Exception:
            return apology(self.request, "Username already exists!")
        x = super().form_valid(form)
        # message = f"""
        # Your Login Credentials for AKT College site are as follows:
        # UserName: {username}
        # Password: {password}
        # You can use these credentials to login to the site.
        # """
        # to = [email]
        # email = EmailMessage("Login Credentials", message, to=to)
        # email.send()
        return x



class RegisterStudent(SuperUserRequiredMixin, CreateView):
    form_class = StudentForm
    model = Student
    success_url = reverse_lazy("college:adminview")
    
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.data.get("password")
        email = form.cleaned_data.get("email")
        # print(username)
        # print(password)
        try:
            User.objects.create_user(username = username, password = password)
        except Exception:
            # form.add_error(username, ValidationError)
            return apology(self.request, "Username already exists!")
        x = super().form_valid(form)
        # message = f"""
        # Your Login Credentials for AKT College site are as follows:
        # UserName: {username}
        # Password: {password}
        # You can use these credentials to login to the site.
        # """
        # to = [email]
        # email = EmailMessage("Login Credentials", message, to=to)
        # email.send()
        return x

class CreateBranch(SuperUserRequiredMixin, CreateView):
    model = Branch
    fields = "__all__"
    success_url = reverse_lazy("college:adminview")


class SuperUserLogin(View):
    def get(self, request):
        return render(request, "accounts/admin_login.html")
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None or not user.is_superuser:
            return apology(request, "Invalid Username or Password")
        # print(user)
        login(request, user)
        return redirect(reverse_lazy("college:adminview"))