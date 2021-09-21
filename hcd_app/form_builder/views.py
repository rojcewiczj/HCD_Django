
from form_builder.models import Program, Question
from django.shortcuts import render, redirect
from .build_question_form import Build_question_form
from .fill_question_form import Fill_question_form

# Create your views here.

def index(request):
    programs = Program.objects.all()
    
    return render(request, "form_builder/index.html", {
        "programs":  programs,
    })

def build_question_view(request, program_id):
    selected_program = Program.objects.get(id = program_id)
    if request.method == "GET":
        build_question_form = Build_question_form()
    else:
        build_question_form = Build_question_form(request.POST)
        if build_question_form.is_valid():
            new_question = build_question_form.save()
            new_question.programs.add(program_id)
            return redirect('build_question_success', program_id=program_id)

    return render(request, 'form_builder/form_question_builder.html', {
        'form': build_question_form,
        'program_id': program_id
    })

def build_question_success(request, program_id):
    return render(request, 'form_builder/build_question_success.html', {
        'program_id': program_id
    })        

def fill_out_form(request, program_id): 
    forms = []
    if request.method == "GET":
        questions = Question.objects.filter(programs = program_id)
        for question in questions:
            question_form = Fill_question_form(instance = question)
            print(question_form)
            forms.append(question_form)
        return render(request, 'form_builder/fill_out_form.html', {
            'forms': forms,
            'program_id': program_id
        })
    elif request.method == "POST":
        fill_question_form = Fill_question_form(request.POST)
        if fill_question_form.is_valid():
            old_question = Question.objects.filter(id = request.POST.id)
            old_question.delete()
            edited_question = fill_question_form.save()
            edited_question.programs.add(program_id)
        return render(request, 'form_builder/fill_out_form.html', {
            'forms': forms,
            'program_id': program_id
        })





    
    
   

def program_options(request, program_id):
    
    return render(request, 'form_builder/program_options.html',{
        'program_id' : program_id
    })