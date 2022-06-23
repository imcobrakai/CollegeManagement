from college.helpers import apology
from college.models import Student, Teacher
from quiz.models import Quiz
from datetime import date
def quiz_valid(request, id):
    try:
        quiz = Quiz.objects.get(id=id)
    except Exception:
        return False
    branch = quiz.author.branch
    student = Student.objects.get(username=request.user)
    return student.branch == branch and quiz.valid_until >= date.today()