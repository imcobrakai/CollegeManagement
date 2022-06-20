from quiz.models import Question, Quiz
from django import forms 

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"
    
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.author = self.request.user
        print(object.author)
        object.save()
        return super(self).form_valid(form)
    
    def form_invalid(self, form):
        print("Called me")

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "option1", "option2", "option3", "option4", "correct"]    