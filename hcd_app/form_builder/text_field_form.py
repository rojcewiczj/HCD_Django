from django import forms
from .models import Question

class Text_field_form(forms.ModelForm):
    
    answer = forms.CharField(min_length=5,max_length= 200)

    class Meta:
        model = Question
        fields = ['id','question','answer']
