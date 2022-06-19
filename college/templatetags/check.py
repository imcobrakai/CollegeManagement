from atexit import register
from django import template
from college.models import Student, Teacher
register = template.Library()

@register.filter
def isTeacher(user):
    isTeacher = False
    try:
        user = Teacher.objects.get(username = user)
        isTeacher = True 
    except Exception:
        isTeacher = False
    return isTeacher

@register.filter
def isStudent(user):
    isStudent = False
    try:
        user = Student.objects.get(username = user)
        isStudent = True 
    except Exception:
        isStudent = False
    return isStudent
