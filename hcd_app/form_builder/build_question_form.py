from django import forms
from .models import Question

answer_format_options = [
    ('text_field', "text field"),
    ('multiple_choice', "multiple choice"),
    ('yes_or_no', "yes or no"),
    ('address_form', "address form"),
]
# form_builder/images/HCD_home.png
img_options = [
     ('None', 'None'),
    ('form_builder\images\3041017803_d58730169a_b.jpeg', 'shower head'),
    ('form_builder\images\bills.jpeg', 'bills'),
    ('form_builder\images\Failure_of_asphalt_shingles_allowing_roof_leakage.jpeg', 'roofing'),
    ('form_builder\images\hvac.jpeg', 'hvac units'),
    ('form_builder\images\Lead-Paint-Abatement-Removal-Clean-up.jpeg', 'chipping paint'),
    ('form_builder\images\3041017803_d58730169a_b.jpeg', 'mold on wall'),
    ('form_builder\images\wheelchair-ramp-disability-access.jpeg', "wheel chair ramp") 
]
class Build_question_form(forms.ModelForm):
    answer_format = forms.MultipleChoiceField(
        choices= answer_format_options,
        widget= forms.CheckboxSelectMultiple()
    )
    img = forms.CharField(
       
        widget= forms.Select( choices= img_options, attrs = {'onchange' : "showImgPreview(this.value);"} )
    )
    class Meta:
        model = Question
        fields = ['question','answer_format', 'img']