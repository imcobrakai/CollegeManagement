from django.contrib import admin
from .models import Quiz, QuizResult, Question
# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Question)