
from form_builder.models import Program, Question, Address
from django.shortcuts import render, redirect
from django.core import serializers

from .question_order_selector import question_order_selector
from .build_question_form import Build_question_form
from .text_field_form import Text_field_form
from .yes_or_no_form import Yes_or_no_form
from .multiple_choice_form import Multiple_choice_helper
from .answer_option_form import Answer_option_form
from formtools.wizard.views import SessionWizardView
from .forms import Address_Form
from .remove_form import Remove_form
# Create your views here.


def index(request):
    programs = Program.objects.all()
    
    return render(request, "form_builder/index.html", {
        "programs":  programs,
    })



def build_question_view(request, program_id):
    programs = Program.objects.all()
    program = None
    img_src = None
    for program in programs:
        if program.id == program_id:
            program = program

    if request.method == "GET":
        build_question_form = Build_question_form()
       
    else:
        build_question_form = Build_question_form(request.POST)
        duplicate = Question.objects.filter(question = request.POST['question'])
        if duplicate:
                return render(request, 'form_builder/form_question_builder.html', {
                    'form': build_question_form,
                    'preview': img_src,
                    'program_id': program_id,
                    'warning' : "you've already asked that question"
                })
        if build_question_form.is_valid(): 
           
            new_question = build_question_form.save()
           
            if request.POST['answer_format'] != 'address_form':
                
                if len(program.question_order) == 0:
                    program.question_order = new_question.question
                    print(program.question_order)
                    
                else:
                    
                    program.question_order += f"/{new_question.question}"
                    
            else: 
                new_address_form = Address_Form()
                if new_address_form.is_valid():
                    new_address_form.save()

                if program.question_order == None:
                    program.question_order = "address_form"
                else:
                    program.question_order += f"/address_form"
            
        program.save()
        new_question.programs.add(program_id)
        if new_question.answer_format[2:-2] == "multiple_choice":
            return redirect("build_question_select_choices", question_id = new_question.id, program_id = program_id)
        
    
    
    return render(request, 'form_builder/form_question_builder.html', {
        'form': build_question_form,
        'preview': img_src,
        'program_id': program_id,
        'warning' : ''
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
        if new_options_added.answer_format == "":
            new_options_added.answer_format += f"{request.POST['option_to_add']}"
        else:
            new_options_added.answer_format += f"/{request.POST['option_to_add']}"
        new_options_added.save()
        print(new_options_added.answer_format)

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
    program = Program.objects.get(id = 5)
    if program.question_order == "" or program.question_order is None:
        return redirect("build_question_view", program_id = program_id)
    current_form_int = int(current_form)
        
    if request.method == "POST":
       
        if back == '1':
            current_form_int -= 1
        elif back == '0':
            current_form_int += 1
            try:
                question_to_edit = Question.objects.get(question = request.POST["question"])
                
                question_to_edit.answer = request.POST['answer']
                if type(request.POST['answer']) is list:
                    print(request.POST) 
                question_to_edit.save()
                
            except:
                address_forms = Address.objects.all()
                if len(address_forms) > 0:
                    address_form = address_forms[0]
                address_form = Address_Form(request.POST) 
                if address_form.is_valid(): 
                    address_form.save()
           
        
    current_form = str(current_form_int) 
    question_order = {}
    current_program = Program.objects.get(id = program_id)
    question_array = current_program.question_order.split("/")
    for i in range(0, len(question_array)):
        question_order[question_array[i]] = str(i)
       
    
    forms = {}
    questions = Question.objects.filter(programs = program_id)
   
    question_ids = [q.question for q in questions]
    for q in questions:
        a_format = q.answer_format
        question_form = ""
        if a_format == "['text_field']":
            question_form = Text_field_form(instance = q)
        elif a_format == "['yes_or_no']":
            question_form = Yes_or_no_form(instance = q)
        elif a_format == "['address_form']":
            question_form = Address_Form()      
            q.question = "address_form"
        else:
            question_form = Multiple_choice_helper(q)
        forms[question_order[q.question]] = [question_form, q.question, q.img, q.second_img]
        
    last_form = str(len(forms) -1)
    
    if int(current_form) > int(last_form):
        print(current_form, last_form)
        return redirect('view_question_submitted', 2)
    
    
    return render(request, 'form_builder/fill_out_form.html', {
        'forms' : forms,
        'last_form' : last_form,
        'current_form' : current_form,
        'program_id': program_id
    })



def view_question_submitted(request, program_id):

    program = Program.objects.get(id = 5)
    questions_submitted = []
    
    structural_issues = {
        'paint' : "structural",
        'roof' : "structural",

    }
 
    eligibility_questions = {
        "Memphis": "ShelbyCounty",
        "income": "IncomeFamily",
        "structural": "StructuralIssues",
        "lead"     : "LeadIssues",
        "live in your home" : "",
        "energy" : "EnergyBurden"
    }
    eligibility_questions_final ={

    }
    questions = Question.objects.all()
    for question in questions:
        if question.answer is not None:
            questions_submitted.append(question)

    income_level = False
    family_size = 0

    for question in questions_submitted:
        for key, value in structural_issues.items():
            if key in question.question:
                eligibility_questions_final[eligibility_questions[structural_issues[key]]] = question.answer
        for key, value in eligibility_questions.items():
            if key in question.question:
                if key == "income":
                    income = int(question.answer)
                    if income < 45000:
                        income_level = True
                elif key == "live in your home":
                    family_size = int(question.answer)
                else:
                    eligibility_questions_final[value] = question.answer
    if income_level == True and family_size > 5:
         eligibility_questions_final["IncomeFamily"] = "yes"      
                        

    address_submitted = [{'fields' : ""}]
    if program.question_order:
        array_order = program.question_order.split("/")
        print(array_order)
        if 'address_form' in array_order:
            address_submitted = serializers.serialize( "python", Address.objects.all() )
            if address_submitted[-1]['fields']['city'] == "Memphis":
                eligibility_questions_final["ShelbyCounty"] = "yes"
            else:
                eligibility_questions_final["ShelbyCounty"] = "no"
        else:
            Address_objects = Address.objects.all()
            for address in Address_objects:
                address.delete()

    
    print(income_level)
    print(eligibility_questions_final)
    return render(request, 'form_builder/view_question_submitted.html',{
        'questions_submitted': questions_submitted,
        'elig_questions': eligibility_questions_final,
        'address_submitted' : address_submitted[0]['fields'],
        'family_size' : family_size,
        'program_id': program_id
    } )


    

def program_options(request, program_id):
    
    return render(request, 'form_builder/program_options.html',{
        'program_id' : program_id
    })

def question_organizer(request, program_id):

    if request.method == "POST":
        
        program = Program.objects.get(id = program_id)
        program.question_order = "/".join(request.POST.getlist('current_location'))
        program.save()
        print(program.question_order)

    program = Program.objects.get(id = program_id)
    current_question_order = program.question_order
   
    question_array = current_question_order.split("/") 
    remove_form = Remove_form(question_array)
    q_dict = {}

    for i in range(len(question_array)):
        q_dict[i] = question_order_selector(i, question_array)

    return render(request, 'form_builder/question_organizer.html',{
        'forms': q_dict,
        'remove_form' : remove_form
    })

def question_remove(request, program_id):
    if request.method == "POST":
       
        program = Program.objects.get(id = program_id)
        question_array = program.question_order.split('/')
        print(question_array)
        for question in question_array:
            if question == request.POST['current_location']:
                question_array.remove(question)
                if question == 'address_form':
                    address_forms = Address.objects.all()
                    for form in address_forms:
                        form.delete()
                    Question.objects.filter(answer_format = "['address_form']").delete()

                Question.objects.filter(question = question).delete()
                
        program.question_order = ("/").join(question_array)
        program.save()
        
                
        
        
        # program.save()
        # print(program.question_order)

    program = Program.objects.get(id = program_id)
    current_question_order = program.question_order
   
    question_array = current_question_order.split("/") 
    remove_form = Remove_form(question_array)
    q_dict = {}

    for i in range(len(question_array)):
        q_dict[i] = question_order_selector(i, question_array)

    return render(request, 'form_builder/question_organizer.html',{
        'forms': q_dict,
        'remove_form' : remove_form
    })
    pass

