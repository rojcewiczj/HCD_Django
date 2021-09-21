from django import forms
from .models import Question

class Build_question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question','answer_format']
