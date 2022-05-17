from django.urls import path
from .views import index, AdminView, StudentView, TeacherView, AttendanceView, StudentList, StudentUpdateView, BranchUpdateView, TeacherUpdateView, StudentDeleteView, BranchDeleteView, TeacherDeleteView
app_name = "college"

urlpatterns = [
    path("", index, name="index"),
    path("adminindex", AdminView.as_view(), name="adminview"),
    path("attendance", AttendanceView.as_view(), name="attendance"),
    path("branchdelete", BranchDeleteView.as_view(), name="branchdelete"),
    path("branchupdate/<int:pk>", BranchUpdateView.as_view(), name="branchupdate"),
    path("studentdelete", StudentDeleteView.as_view(), name="studentdelete"),
    path("studentindex/<int:pk>", StudentView.as_view(), name="studentview"),
    path("studentlist", StudentList.as_view(), name="studentlist"),
    path("studentupdate/<int:pk>", StudentUpdateView.as_view(), name="studentupdate"),
    path("teacherdelete", TeacherDeleteView.as_view(), name="teacherdelete"),
    path("teacherindex/<int:pk>", TeacherView.as_view(), name="teacherview"),
    path("teacherupdate/<int:pk>", TeacherUpdateView.as_view(), name="teacherupdate"),
]
