from datetime import date
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views import View
from requests import request
from college.models import Student, Teacher
from quiz.forms import QuestionForm, QuizForm
from accounts.views import StudentLoginRequiredMixin, TeacherLoginRequiredMixin
from quiz.models import Question, Quiz, QuizResult
from quiz.helper import quiz_valid
from college.helpers import apology
# Create your views here.
class CreateQuiz(TeacherLoginRequiredMixin, View):
    def get(self, request):
        form = QuizForm()
        content = {
            "form": form,
            "teacher": Teacher.objects.get(username=request.user),
        }
        return render(request, "quiz/options.html", content)

    def post(self, request):
        quizform = QuizForm(request.POST)
        # quizform.form_valid(quizform)
        # print(dir(quizform))
        print(request.POST)
        print(quizform.errors)
        if not quizform.is_valid():
            print("hello")
            content = {
                "form": quizform,
            }
            return render(request, "quiz/options.html", content)
        object = quizform.save()
        
        form = QuestionForm()
        context = {
            "number": range(int(request.POST.get("questions"))),
            "count": int(request.POST.get("questions")),
            "duration": request.POST.get("duration"),
            "form": form,
            "quiz": object,
        }
        return render(request, "quiz/questions.html", context)

class AddQuestions(View):
    def get(self, request):
        return redirect(reverse_lazy("quiz:createquiz"))

    def post(self, request):
        count = int(request.POST.get("count"))
        for i in range(count):
            text = request.POST.get("text" + str(i + 1))
            optiona = request.POST.get("optiona" + str(i + 1))
            optionb = request.POST.get("optionb" + str(i + 1))
            optionc = request.POST.get("optionc" + str(i + 1))
            optiond = request.POST.get("optiond" + str(i + 1))
            correctopt = request.POST.get("correct" + str(i + 1))
            correct = request.POST.get(correctopt)
            quiz = Quiz.objects.get(id=int(request.POST.get("quiz")))
            Question.objects.create(text=text, option1=optiona, option2=optionb, option3=optionc, option4=optiond, correct=correct, quiz=quiz)
        return redirect(reverse_lazy("college:teacherview"))

class QuizList(StudentLoginRequiredMixin, ListView):    
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz_list"] = context["quiz_list"].filter(valid_until__gte=date.today())
        branch = Student.objects.get(username=self.request.user).branch
        teachers = Teacher.objects.filter(branch = branch)
        context["quiz_list"] = context["quiz_list"].filter(author__in=teachers)
        return context
    
class AttemptQuiz(StudentLoginRequiredMixin, View):
    def get(self, request, id):
        try:
            quiz = Quiz.objects.get(id=id)
        except Exception:
            return apology(request, "Invalid quiz")
        if not quiz_valid(request, id):
            return apology(request, "Invalid quiz")
        questions = Question.objects.filter(quiz=quiz)

        try:
            if QuizResult.objects.get(quiz=quiz, student_name=Student.objects.get(username=request.user)):
                return apology(request, "You already attempted this quiz!")
        except Exception:
            attempted = False
        count = range(len(questions))
        
        context = {
            "questions": zip(questions, count),
            "attempted": attempted,
            "duration": quiz.duration,
        }
        return render(request, "quiz/attempt.html", context)
    
    def post(self, request, id):
        try:
            quiz = Quiz.objects.get(id=id)
        except Exception:
            return apology(request, "Invalid quiz")
        questions = Question.objects.filter(quiz=quiz)
        score = 0
        for i in range(len(questions)):
            correctopt = request.POST.get("correct" + str(i + 1))
            if correctopt == questions[i].correct:
                score += 1
        student = Student.objects.get(username= request.user)
        QuizResult.objects.create(quiz=quiz, student_name=student, marks = score)
        
        return redirect(reverse_lazy("quiz:result", kwargs={"id":id}))

class QuizesList(TeacherLoginRequiredMixin, View):
    def get(self, request):
        try:
            quizes = Quiz.objects.filter(author=Teacher.objects.get(username=request.user))
        except Exception:
            return apology(request, "Quiz does not exist")
        context = {
            "quizes": quizes 
        }
        return render(request, "quiz/quizes_list.html", context)

class QuizResults(TeacherLoginRequiredMixin, View):
    def get(self, request, id):
        
        try:
            quiz = Quiz.objects.get(id=id)
            count = Question.objects.filter(quiz=quiz).count()
            if quiz.author.username != str(request.user):
                return apology(request, "Invalid Quiz")
            results = QuizResult.objects.filter(quiz=quiz)
        except Exception:
            return apology(request, "Invalid Quiz")
        
        context = {
            "results": results,
            "count": count,
        }
        return render(request, "quiz/result_list.html", context)

class Result(StudentLoginRequiredMixin ,View):
    def get(self, request, id):
        try: 
            quiz = Quiz.objects.get(id=id)
            result = QuizResult.objects.get(quiz=quiz, student_name=Student.objects.get(username=request.user))
            count = Question.objects.filter(quiz=quiz).count()
        except Exception:
            return apology(request, "Result Unavailable")
        context = {
            "score": result.marks,
            "total": count,
        }
        return render(request, "quiz/result.html", context)
