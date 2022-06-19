from .models import Teacher, Student, Branch
from accounts.views import StudentLoginRequiredMixin, SuperUserRequiredMixin, TeacherLoginRequiredMixin
from college.helpers import apology
from django.contrib.auth.models import User
from accounts.forms import TeacherForm, StudentForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
# Create your views here.
def index(request):
    # if request.method == "GET":
        # form = StudentForm()
    return render(request, "college/index.html")
    # form = StudentForm(request.POST)
    # form.save()
    # print(form.is_valid())
    # if form.is_valid():
    #     print("hello")
    #     print(form.cleaned_data.get("prn"))
    #     print(form.cleaned_data.get("username"))
    #     print(form.cleaned_data.get("password"))
    # for error in form.errors:
    #     print(error)
    # if form.has_error():
        # print("hello")
    # return render(request, "college/index.html", {"form": form})

class AdminView(SuperUserRequiredMixin, ListView):
    model = Teacher
    template_name = "college/admin_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_list = Student.objects.all()
        student_count = Student.objects.all().count()
        teacher_count = Teacher.objects.all().count()
        branch_count = Branch.objects.all().count()
        branches = Branch.objects.all()
        branch_list = []
        for branch in branches:
            st_count = Student.objects.filter(branch = branch).count()
            tc_count = Teacher.objects.filter(branch=branch).count()
            branch_list.append({
                'branch': branch,
                'teacher_count': tc_count,
                'student_count': st_count,
            })
        context["student_list"] = student_list
        context["branch_list"] = branch_list
        context["student_count"] = student_count
        context["teacher_count"] = teacher_count
        context["branch_count"] = branch_count
        return context

class StudentView(StudentLoginRequiredMixin, DetailView):
    model = Student
    template_name = "college/student_index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = Student.objects.get(username = self.request.user) 
        return context

class TeacherView(TeacherLoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "college/teacher_index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher"] = Teacher.objects.get(username = self.request.user) 
        return context
    
    

class AttendanceView(TeacherLoginRequiredMixin, View):
    def get(self, request):
        branch = (Teacher.objects.values("branch").get(username = request.user))["branch"]
        student_list = Student.objects.filter(branch= branch)
        context = {
            "student_list": student_list,
            'pk': Teacher.objects.values('id').get(username = request.user)['id'],
        }
        return render(request, "college/attendance.html", context)
    def post(self, request):
        branch = (Teacher.objects.values("branch").get(username = request.user))["branch"]
        student_list = Student.objects.filter(branch= branch)
        # print("Hello")
        for student in student_list:
            was_present = request.POST.get(student.name)
            if was_present == "yes":
                student.lectures_attended += 1
            student.total_lectures += 1
            student.save()
        return redirect(reverse_lazy("college:teacherview", kwargs={'pk': Teacher.objects.values('id').get(username = request.user)['id']}))

class StudentList(TeacherLoginRequiredMixin, ListView):
    model = Student
    template_name = "college/student_list.html"
    
    def get_queryset(self):
        branch = (Teacher.objects.values("branch").get(username = self.request.user))["branch"]
        return super().get_queryset().filter(branch = branch)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class StudentUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Student
    template_name = "college/student_update_form.html"    
    success_url = reverse_lazy("college:adminview")
    fields = ["name", "prn", "branch", "email"]

class TeacherUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Teacher
    template_name = "college/teacher_update_form.html"    
    success_url = reverse_lazy("college:adminview")
    fields = ["name", "branch", "email"]

class BranchUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Branch
    template_name = "college/branch_update_form.html"    
    success_url = reverse_lazy("college:adminview")
    fields = ["name"]

class StudentDeleteView(SuperUserRequiredMixin, View):
    def get(self, request):
        return redirect(reverse_lazy("college:adminview"))
    
    def post(self, request):
        student_id = request.POST.get("id")
        try: 
            student = Student.objects.get(id = student_id)
            username = student.username
            user = User.objects.get(username=username)
            student.delete()
            user.delete()
        except:
            return apology("Student Not Found!")
        return redirect(reverse_lazy("college:adminview"))
class TeacherDeleteView(SuperUserRequiredMixin, View):
    def get(self, request):
        return redirect(reverse_lazy("college:adminview"))
    
    def post(self, request):
        teacher_id = request.POST.get("id")
        try: 
            teacher = Teacher.objects.get(id = teacher_id)
            username = teacher.username
            user = User.objects.get(username=username)
            teacher.delete()
            user.delete() 
        except:
            return apology("Student Not Found!")
        return redirect(reverse_lazy("college:adminview"))


class BranchDeleteView(SuperUserRequiredMixin, View):
    def get(self, request):
        return redirect(reverse_lazy("college:adminview"))
    
    def post(self, request):
        branch_id = request.POST.get("id")
        try: 
            branch = Branch.objects.get(id = branch_id)
            branch.delete() 
        except:
            return apology("Branch Not Found!")
        return redirect(reverse_lazy("college:adminview"))