from django.urls import path
from .views import CreateQuiz, AddQuestions, QuizList, AttemptQuiz

app_name = "quiz"
urlpatterns = [
    path("create/", CreateQuiz.as_view(), name="createquiz"),
    path("addquestions/", AddQuestions.as_view(), name="addquestions"),
    path("available/", QuizList.as_view(), name="available"),
    path("attempt/<int:id>", AttemptQuiz.as_view(), name="attempt"),
]
