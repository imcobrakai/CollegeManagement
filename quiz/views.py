from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from college.models import Teacher
from quiz.forms import QuestionForm, QuizForm
from accounts.views import TeacherLoginRequiredMixin
from quiz.models import Question, Quiz
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