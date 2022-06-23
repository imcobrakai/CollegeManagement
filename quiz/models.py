from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import SelectDateWidget
from college.models import Teacher, Student
from django.conf import settings
# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(validators=[MinValueValidator(1, "Duration should be greater than or equal to 1")])
    questions = models.IntegerField(validators=[MinValueValidator(1, "Number of questions should be greater than or equal to 1")])
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    valid_until = models.DateField()

    def __str__(self):
        return self.name
    

class Question(models.Model):
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class QuizResult(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField()
    