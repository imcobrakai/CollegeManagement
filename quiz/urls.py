from django.urls import path
from .views import CreateQuiz, AddQuestions, QuizList, AttemptQuiz, QuizesList, QuizResults, Result

app_name = "quiz"
urlpatterns = [
    path("create/", CreateQuiz.as_view(), name="createquiz"),
    path("addquestions/", AddQuestions.as_view(), name="addquestions"),
    path("available/", QuizList.as_view(), name="available"),
    path("attempt/<int:id>", AttemptQuiz.as_view(), name="attempt"),
    path("list/", QuizesList.as_view(), name="quizlist"),
    path("results/<int:id>", QuizResults.as_view(), name="results"),
    path("result/<int:id>", Result.as_view(), name="result"),
]
