from . import views
from django.urls import path





urlpatterns = [
    path('form_builder/', views.index, name="all-programs"), #our-domain.com/form_builder,
    path('form_builder/program_options/<program_id>', views.program_options, name="program_options"),
    path('form_builder/build_question/<program_id>', views.build_question_view, name="build_question_view"),
    path('form_builder/ajax_build_question/<program_id>', views.ajax_build_question_view, name="ajax_build_question_view"),
    path('form_builder/fill_question/<program_id>/<current_form>/<back>', views.fill_out_form, name="fill_out_form"),
    path('form_builder/select_choices/<program_id>/<question_id>', views.build_question_select_choices, name="build_question_select_choices" ),
    path('form_builder/build_question_success/<program_id>', views.build_question_success, name="build_question_success"),
    path('form_builder/view_question_submitted/<program_id>', views.view_question_submitted, name="view_question_submitted"),
    path('form_builder/question_organizer/<program_id>', views.question_organizer, name = "question_organizer")

     ##our-domain.com/form_builder/<program_name>
]