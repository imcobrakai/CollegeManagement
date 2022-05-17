from django.db import models
# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100, null=False)
    prn = models.IntegerField(null=False, unique=True)
    lectures_attended = models.IntegerField(default=0)
    total_lectures = models.IntegerField(default=0)
    branch = models.ForeignKey("Branch", models.CASCADE)
    username = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(null=True)

class Teacher(models.Model):
    name = models.CharField(max_length=100, null=False)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE, null=False)
    username = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(null=True)

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name