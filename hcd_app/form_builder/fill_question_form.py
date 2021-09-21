from django import forms
from .models import Question

class Fill_question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['id','question','answer']
