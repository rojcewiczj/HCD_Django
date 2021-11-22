from . import views
from django.urls import path





urlpatterns = [
    path('form_builder/', views.index, name="all-forms"), #our-domain.com/form_builder,
    path('form_builder/form_options/<custom_form_id>', views.custom_form_options, name="form_options"),
    path('form_builder/create_program/', views.create_program, name="create_program"),
    path('form_builder/create_statement/<program_id>', views.create_statement, name="create_statement"),
    path('form_builder/create_requirement/<statement_id>', views.create_statement, name="create_statement"),
    path('form_builder/resources/<custom_form_id>', views.resource_view, name="resource_view"),
    path('form_builder/resources/build_question/<custom_form_id>', views.build_question_view, name="build_question_view"),
    path('form_builder/fill_question/<custom_form_id>/<current_form>/<back>', views.fill_out_form, name="fill_out_form"),
    path('form_builder/select_choices/<custom_form_id>/<question_id>', views.build_question_select_choices, name="build_question_select_choices" ),
    path('form_builder/build_question_success/<custom_form_id>', views.build_question_success, name="build_question_success"),
    path('form_builder/view_question_submitted/<custom_form_id>', views.view_question_submitted, name="view_question_submitted"),
    path('form_builder/question_organizer/<custom_form_id>/<order_or_remove>', views.question_organizer, name = "question_organizer"),
    path('form_builder/question_remove/<custom_form_id>', views.question_remove, name = "question_remove")

     ##our-domain.com/form_builder/<form_name>
]