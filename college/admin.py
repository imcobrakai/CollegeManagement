from django.contrib import admin
from .models import Branch, Student, Teacher
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Branch)