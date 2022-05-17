from django.urls import path
from .views import RegisterTeacher, TeacherLogin, StudentLogin, RegisterStudent, SuperUserLogin, CreateBranch
app_name = "accounts"

urlpatterns = [
    path("createteacher", RegisterTeacher.as_view(), name="createteacher"),
    path("createstudent", RegisterStudent.as_view(), name="createstudent"),
    path("teacherlogin", TeacherLogin.as_view(), name="loginteacher"),
    path("studentlogin", StudentLogin.as_view(), name="loginstudent"),
    path("adminlogin", SuperUserLogin.as_view(), name="loginadmin"),
    path("createbranch", CreateBranch.as_view(), name="createbranch"),
    
]
