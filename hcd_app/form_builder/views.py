from form_builder.models import Program, Question
from django.shortcuts import render
from django.http import HttpResponse
from .build_question_form import Build_question_form
# Create your views here.

def index(request):
    programs = Program.objects.all()
    
    return render(request, "form_builder/index.html", {
        "programs":  programs,
    })

def build_question_view(request):
    
    build_question_form = Build_question_form()
    return render(request, 'form_builder/form_question_builder.html', {
        'build_question_form': build_question_form
    })
    
   

def program_options(request, program_id):
    return render(request, 'form_builder/program_options.html')