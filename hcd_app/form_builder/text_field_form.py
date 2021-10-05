from typing import Text
from django import forms
from .models import Question
from django.forms import ModelForm, TextInput, EmailInput
class Text_field_form(forms.ModelForm):
    
    answer = forms.CharField(min_length=5,max_length= 200)

    class Meta:
        model = Question
        fields = ['id','question','answer']
        widgets = {
            'answer': TextInput(attrs={
                'style': 'width: 635px; height: 28px; left: 12px; font-family: Arial; font-style: normal; font-weight: normal; font-size: 36px;line-height: 41px;',
                'placeholder': 'answer'
                }),
            'question': TextInput(attrs={
                'style': ' visibility: hidden; hight: 0px;',
                'placeholder': 'question'
                }),
            
        } 