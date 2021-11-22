from django import forms
from .models import Question

answer_format_options = [
    ('text_field', "text field"),
    ('multiple_choice', "multiple choice"),
    ('yes_or_no', "yes or no"),
    ('address_form', "address form"),
]
# form_builder/images/HCD_home.png



#currently images are being stored in image folder
img_options = [
     ('None', 'None'),
    ('form_builder\images\B3041017803_d58730169a_b.jpeg', 'shower head'),
   ('form_builder\images\Bills.jpeg', 'bills'),
    ('form_builder\images\Failure_of_asphalt_shingles_allowing_roof_leakage.jpeg', 'roofing'), 
    ('form_builder\images\hvac.jpeg', 'hvac units'),
    ('form_builder\images\Lead-Paint-Abatement-Removal-Clean-up.jpeg', 'chipping paint'),
    ('form_builder\images\Mold_on_wall2.jpeg', 'mold on wall'),
    ('form_builder\images\wheelchair-ramp-disability-access.jpeg', "wheel chair ramp"),
    ('form_builder\images\electrical.png', "light switch"),
    ('form_builder\images\ceiling.png', "cracked ceiling"),
    ('form_builder\images\BrokenPipe.png', "leaky plumbing"),
    ('form_builder\images\DirtyFilter.png', "dirty filter"),
    ('form_builder\images\MLGWbill.jpg', "MLGW bill"),
    ('form_builder\images\MoldCeiling.png', "mold on ceiling"),
    ('form_builder\images\MildewSurface.png', "mildew on surface"),
    ('form_builder\images\MildChipping.png', "mild paint chipping"),
    ('form_builder\images\SevereChipping.png', "severe paint chipping"),
    ('form_builder\images\SupportRail.png', "support rail"),
    ('form_builder\images\Wheelchair.png', "person in wheelchair")

]
# form for building questions
class Build_question_form(forms.ModelForm):
    answer_format = forms.MultipleChoiceField(
        choices= answer_format_options,
        widget= forms.RadioSelect()
    )
    img = forms.CharField(
       
        widget= forms.Select( choices= img_options, attrs = {'onchange' : "showImgPreview(this.value);"} )
    )
    second_img = forms.CharField(
       
        widget= forms.Select( choices= img_options, attrs = {'onchange' : "showSecondImgPreview(this.value);"} )
    )
    class Meta:
        model = Question
        fields = ['question','answer_format', 'img', 'second_img']