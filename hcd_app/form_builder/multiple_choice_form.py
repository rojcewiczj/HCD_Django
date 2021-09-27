from django import forms
from .models import Question

class Multiple_choice_form(forms.ModelForm):
    
    def __init__(self, answer_format):
        def get_options(self, answer_format):
            answer_options = []
            opts = answer_format.split(" ")
            for opt in opts:
                answer_options.append((opt, opt))

        self.answer = forms.MultipleChoiceField(choices = get_options(answer_format))
    
    
    # answer_options = []
   
    # options = []
    # string_format = str(Question.answer_format)
    # options = string_format.split(" ")
    # for option in options:
    #     answer_options.append((option,option))
    # answer = forms.MultipleChoiceField(choices= answer_options)

    class Meta:
        model = Question
        fields = ['id','question','answer']