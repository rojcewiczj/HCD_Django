
from form_builder.models import Program, Question
from django.shortcuts import render, redirect
from .build_question_form import Build_question_form
from .text_field_form import Text_field_form
from .yes_or_no_form import Yes_or_no_form
from .multiple_choice_form import Multiple_choice_form
from .answer_option_form import Answer_option_form

# Create your views here.
answer_options = []

def index(request):
    programs = Program.objects.all()
    
    return render(request, "form_builder/index.html", {
        "programs":  programs,
    })

def build_question_view(request, program_id):
    
    if request.method == "GET":
        build_question_form = Build_question_form()
    else:
        build_question_form = Build_question_form(request.POST)
        if build_question_form.is_valid():
            new_question = build_question_form.save()
            new_question.programs.add(program_id)
            print(new_question.id)
            if new_question.answer_format[2:-2] == "multiple_choice":
                return redirect("build_question_select_choices", question_id = new_question.id)
            return redirect('build_question_success', program_id=program_id)

    return render(request, 'form_builder/form_question_builder.html', {
        'form': build_question_form,
        'program_id': program_id
    })

def build_question_select_choices(request, question_id):
    print(question_id)
    question_to_edit = Question.objects.get(id = question_id)
    
    if request.method == "GET":
        answer_option_form = Answer_option_form(question_to_edit)
    else:
        print(request.POST)
        new_options_added = question_to_edit
        new_options_added.answer_format += f" {request.POST['option_to_add']}"
        new_options_added.save()

        answer_option_form = Answer_option_form(question_to_edit)
    return render(request, "form_builder/multiple_choice_builder.html", {
        "question_id" : question_id,
        'form' : answer_option_form,
        'question' : question_to_edit.question
    })






def build_question_success(request, program_id):
    return render(request, 'form_builder/build_question_success.html', {
        'program_id': program_id
    })        

def fill_out_form(request, program_id): 
    forms = []
    questions = Question.objects.filter(programs = program_id)
    for question in questions:
        a_format = question.answer_format[2:-2]
        if a_format == 'text_field':
            question_form = Text_field_form(instance = question)
        elif a_format == 'yes_or_no':
            print("yes_or_no_form")
            question_form = Yes_or_no_form(instance = question)
        else:
            question_form = Multiple_choice_form(a_format)
        forms.append(question_form)
    if request.method == "POST":
        print(request)

        if answer_format == "text_field":
            fill_question_form = Text_field_form(request.POST)
        if answer_format == "yes_or_no_field":
            fill_question_form = Yes_or_no_form(request.POST)
            fill_question_form.answer = str(fill_question_form.answer)
        if answer_format == "multiple_choice":
            fill_question_form = Multiple_choice_form(request.POST)

        if fill_question_form.is_valid():
            old_questions = Question.objects.filter(question = request.POST['question'])
            for q in old_questions:
                q.delete()
            edited_question = fill_question_form.save()
            edited_question.programs.add(program_id)
    return render(request, 'form_builder/fill_out_form.html', {
        'forms': forms,
        'program_id': program_id
    })

def view_question_submitted(request, program_id):
    questions_submitted = []
    questions = Question.objects.filter(programs = program_id)
    for question in questions:
        if question.answer is not None:
            questions_submitted.append(question)
    return render(request, 'form_builder/view_question_submitted.html',{
        'questions_submitted': questions_submitted,
        'program_id': program_id
    } )







    
    
   

def program_options(request, program_id):
    
    return render(request, 'form_builder/program_options.html',{
        'program_id' : program_id
    })