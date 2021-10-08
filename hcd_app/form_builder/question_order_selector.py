from django import forms



def question_order_selector(i, question_array):
    question_choices = []
    
    for q in question_array:
        question_choices.append((q, q))
    

    class question_order_form(forms.Form):
        current_location = forms.CharField(label=f'{i + 1}', widget=forms.Select(choices= question_choices))
    
    return question_order_form(initial={'current_location': f'{question_array[i]}'})

