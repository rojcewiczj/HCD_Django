from django import forms

def Remove_form(question_array):
    question_choices = []
    
    for q in question_array:
        question_choices.append((q, q))
    

    class question_order_form(forms.Form):
        current_location = forms.CharField(label='Remove Question', widget=forms.Select(choices= question_choices))
    
    return question_order_form()