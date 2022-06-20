from django.urls import path
from .views import CreateQuiz, AddQuestions

app_name = "quiz"
urlpatterns = [
    path("create/", CreateQuiz.as_view(), name="createquiz"),
    path("addquestions/", AddQuestions.as_view(), name="addquestions"),
]
