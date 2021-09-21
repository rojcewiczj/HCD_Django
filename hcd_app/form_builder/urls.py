from . import views
from django.urls import path
 
urlpatterns = [
    path('form_builder/', views.index, name="all-programs"), #our-domain.com/form_builder,
    path('form_builder/program_options/<program_id>', views.program_options, name="program_options"),
    path('form_builder/build_question/', views.build_question_view, name="build_question_view")
     ##our-domain.com/form_builder/<program_name>
]