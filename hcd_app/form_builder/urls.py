from . import views
from django.urls import path
 
urlpatterns = [
    path('form_builder/', views.index, name="all-programs"), #our-domain.com/form_builder,
    path('form_builder/program_options/<program_id>', views.program_options, name="program_options"),
    path('form_builder/build_question/<program_id>', views.build_question_view, name="build_question_view"),
    path('form_builder/fill_question/<program_id>', views.fill_out_form, name="fill_question_view"),
    path('form_builder/build_question_success/<program_id>', views.build_question_success, name="build_question_success")
     ##our-domain.com/form_builder/<program_name>
]