
from form_builder.models import Program, Question
from django.shortcuts import render, redirect
from .build_question_form import Build_question_form
from .text_field_form import Text_field_form
from .yes_or_no_form import Yes_or_no_form
from .multiple_choice_form import Multiple_choice_helper
from .answer_option_form import Answer_option_form
from formtools.wizard.views import SessionWizardView

# Create your views here.
# def getForms():
#     form_list = [] 
#     questions = Question.objects.filter(programs = 2)
#     for question in questions:
#         if question.answer == None:
#             a_format = question.answer_format
#             question_form = ""
#             if a_format == "['text_field']":
#                 question_form = Text_field_form(instance = question)
#             elif a_format == "['yes_or_no']":
#                 question_form = Yes_or_no_form(instance = question)
                
#             else:
#                 question_form = Multiple_choice_helper(question)
                
#             form_list.append(question_form)
#     return form_list

# class order_wizard(SessionWizardView):
#     template_name = "form_builder/form_wizard.html"
#     form_list = getForms()
#     def done(self, form_list, **kwargs):
#         return render(self.request, 'done.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })

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
            if new_question.answer_format[2:-2] == "multiple_choice":
                return redirect("build_question_select_choices", question_id = new_question.id, program_id = program_id)
            return redirect('build_question_success', program_id=program_id)

    return render(request, 'form_builder/form_question_builder.html', {
        'form': build_question_form,
        'program_id': program_id
    })

def build_question_select_choices(request, program_id, question_id):
    print(question_id)
    question_to_edit = Question.objects.get(id = question_id)
    
    if request.method == "GET":
        answer_option_form = Answer_option_form(question_to_edit)
    else:
        new_options_added = question_to_edit
        if new_options_added.answer_format == "['multiple_choice']":
            new_options_added.answer_format = ""
        
        new_options_added.answer_format += f" {request.POST['option_to_add']}"
        new_options_added.save()

        answer_option_form = Answer_option_form(question_to_edit)
    return render(request, "form_builder/multiple_choice_builder.html", {
        "program_id" : program_id,
        "question_id" : question_id,
        'form' : answer_option_form,
        'question' : question_to_edit.question
    })



def build_question_success(request, program_id):
    return render(request, 'form_builder/build_question_success.html', {
        'program_id': program_id
    })        


        
def fill_out_form(request, program_id, current_form , back): 
    print(type(current_form))
    
        
    if request.method == "POST":
        if back == '0':
            print("back is 0")
            current_form_int = int(current_form)
            current_form_int += 1
            current_form = str(current_form_int)
            question_to_edit = Question.objects.get(question = request.POST["question"])
            id = question_to_edit.id
            new_question = question_to_edit
            new_question.answer = request.POST['answer']
            print(id)
            question_to_edit.delete()
            new_question.save()
            new_question.programs.add(program_id)
        elif back == '1':
            print(current_form)
            current_form_int = int(current_form)
            current_form_int -= 1
            print(current_form_int)
            current_form = str(current_form_int)
        
    
    forms = {}

    questions = Question.objects.filter(programs = program_id)
    question_ids = [q.id for q in questions]
    print(question_ids)
    for i in range(0, len(questions)):
        a_format = questions[i].answer_format
        question_form = ""
        if a_format == "['text_field']":
            question_form = Text_field_form(instance = questions[i])
        elif a_format == "['yes_or_no']":
            question_form = Yes_or_no_form(instance = questions[i])
                
        else:
            question_form = Multiple_choice_helper(questions[i])
                
        forms[f'{i}'] = question_form
        
    
    
    return render(request, 'form_builder/fill_out_form.html', {
        'forms' : forms,
        'current_form' : current_form,
        'program_id': program_id
    })



def view_question_submitted(request, program_id):
    questions_submitted = []
    questions = Question.objects.all()
    for question in questions:
        for program in question.programs.all():
            if str(program.id) == program_id and question.answer is not None:
                questions_submitted.append(question)
    return render(request, 'form_builder/view_question_submitted.html',{
        'questions_submitted': questions_submitted,
        'program_id': program_id
    } )


    

def program_options(request, program_id):
    
    return render(request, 'form_builder/program_options.html',{
        'program_id' : program_id
    })