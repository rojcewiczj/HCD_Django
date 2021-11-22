from django import forms
from django.forms import widgets
from .models import Address, Question
from django.forms.widgets import CheckboxSelectMultiple, TextInput

# this file is not currently being used but the idea was to move all the form classes into this file

answer_format_options = [
    ('text_field', "text field"),
    ('multiple_choice', "multiple choice"),
    ('yes_or_no', "yes or no"),
    ('address_form', "address form"),
]

class Build_question_form(forms.ModelForm):
    answer_format = forms.MultipleChoiceField(choices= answer_format_options)
    class Meta:
        model = Question
        fields = ['question','answer_format']



class Text_field_form(forms.ModelForm):
    
    answer = forms.CharField(min_length=5,max_length= 200)

    class Meta:
        model = Question
        fields = ['id','question','answer']



def Multiple_choice_helper(question):   
    options = []
    opts = question.answer_format[1:].split(" ")
    for opt in opts:
        options.append((opt, opt))
   

    class Multiple_choice_form(forms.ModelForm):
        
        answer = forms.MultipleChoiceField(
            
            choices= options
        )
        
        
        
        class Meta:
            model = Question
            fields = ['question','answer']

    return Multiple_choice_form(instance=question)



class Yes_or_no_form(forms.ModelForm):
   
    yes_or_no = [
        ("yes" , "Yes"),
        ("no" , "No")
    ]
    answer = forms.MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices= yes_or_no
    )
    

    class Meta:
        model = Question
        fields = ['id','question','answer']


class Answer_option_form(forms.Form):
       
    def __init__(self, new_question):
        self.question = new_question.question
        self.option_to_add = forms.CharField(label="add and answer option to the multiple choice", max_length= 50)

class Address_Form(forms.ModelForm):
    

    class Meta:
        model = Address
        fields = ['address_1','address_2','city','state','zip_code', 'build_date']
        # widgets ={
        #     'address_1': TextInput(attrs={
        #         'style': 'width: 635px; height: 28px;left: 12px; top: 10px;',
        #         'placeholder': 'answer'
        #         }),
        #     'address_2':TextInput(attrs={
        #         'style': 'width: 635px; height: 28px;left: 12px; top: 10px;',
        #         'placeholder': 'answer'
        #         }),
        #     'city':TextInput(attrs={
        #         'style': 'width: 635px; height: 28px;left: 12px; top: 10px;',
        #         'placeholder': 'answer'
        #         }),
        #     'state':TextInput(attrs={
        #         'style': 'width: 100px; height: 28px;left: 12px; top: 10px;',
        #         'placeholder': 'answer'
        #         }),
        #     'zip_code':TextInput(attrs={
        #         'style': 'width: 386px; height: 28px;left: 12px; top: 10px;',
        #         'placeholder': 'answer'
        #         }),
        #     'build_date':TextInput(attrs={
        #         'style': 'width: 100px; height: 28px;left: 12px; top: 10px;',
        #         'placeholder': 'answer'
        #         }),
        # }



         