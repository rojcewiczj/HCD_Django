from django import forms


# form for adding answer options to the multiple choice questions
class Answer_option_form(forms.Form):
       
    def __init__(self, new_question):
        self.question = new_question.question
        self.option_to_add = forms.CharField(label="add and answer option to the multiple choice", max_length= 50)
    