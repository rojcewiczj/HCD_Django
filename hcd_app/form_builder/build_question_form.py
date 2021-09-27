from django import forms
from .models import Question

answer_format_options = [
    ('text_field', "text field"),
    ('multiple_choice', "multiple choice"),
    ('yes_or_no', "yes or no"),
]
class Build_question_form(forms.ModelForm):
    answer_format = forms.MultipleChoiceField(choices= answer_format_options)
    class Meta:
        model = Question
        fields = ['question','answer_format']