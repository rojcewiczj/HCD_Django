from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Question
from django.forms import ModelForm, TextInput, EmailInput

class Yes_or_no_form(forms.ModelForm):
    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        if value and self.max_choices and len(value) > self.max_choices:
            raise forms.ValidationError('You must select a maximum of %s choice%s.')
                   
        return value
    
    # if forms.ModelForm.answer_format == "text_field":
    #     answer = forms.CharField(min_length=5,max_length= 200)
    yes_or_no = [
        ("yes" , "Yes"),
        ("no" , "No")
    ]
    answer = forms.ChoiceField(
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
        widgets = {
            'answer': TextInput(attrs={
                'style': 'width: 635px; height: 28px; left: 12px; top: 10px; font-family: Arial; font-style: normal; font-weight: normal; font-size: 50px;line-height: 41px;',
                'placeholder': 'answer'
                }),
            'question': TextInput(attrs={
                'style': ' visibility: hidden;',
                'placeholder': 'question'
                }),
            }