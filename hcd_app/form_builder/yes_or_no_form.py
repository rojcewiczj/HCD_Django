from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Question

class Yes_or_no_form(forms.ModelForm):
   
    
    # if forms.ModelForm.answer_format == "text_field":
    #     answer = forms.CharField(min_length=5,max_length= 200)
    yes_or_no = [
        ("yes" , "Yes"),
        ("no" , "No")
    ]
    answer = forms.MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices= yes_or_no
    )
    # else:
    #     options = []
    #     string_format = str(Question.answer_format)
    #     options = string_format.split(" ")
    #     for option in options:
    #         answer_options.append((option,option))
    #     answer = forms.MultipleChoiceField(choices= answer_options)
    # def __init__(self):
    #     if Question.answer_format == "yes_or_no":
    #         self.fields['answer'].initial  = False

    class Meta:
        model = Question
        fields = ['id','question','answer']