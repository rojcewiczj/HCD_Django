
from django.db.models.query import QuerySet
from form_builder.models import Custom_Form, Question, Address
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
    custom_forms = Custom_Form.objects.all()
    
    return render(request, "form_builder/index.html", {
        "custom_forms":  custom_forms,
    })


def resource_view(request, custom_form_id):
    
    return render(request, 'form_builder/resources.html')
        
    


def build_question_view(request, custom_form_id):
    custom_forms = Custom_Form.objects.all()
    custom_form = None
    img_src = None
    for custom_form in custom_forms:
        if custom_form.id == custom_form_id:
            custom_form = custom_form

    if request.method == "GET":
        build_question_form = Build_question_form()
       
    else:
        
        build_question_form = Build_question_form(request.POST)
        duplicate = Question.objects.filter(question = request.POST['question'])
        if duplicate:
                return render(request, 'form_builder/form_question_builder.html', {
                    'form': build_question_form,
                    'preview': img_src,
                    'custom_form_id': custom_form_id,
                    'warning' : "you've already asked that question"
                    })
        

        if build_question_form.is_valid(): 
           
            new_question = build_question_form.save()
           
            if request.POST['answer_format'] != 'address_form':
                
                if len(Custom_Form.question_order) == 0:
                    Custom_Form.question_order = new_question.question
                    (Custom_Form.question_order)
                    
                else:
                    
                    Custom_Form.question_order += f"/{new_question.question}"
                    
            else: 
                new_address_form = Address_Form()
                if new_address_form.is_valid():
                    new_address_form.save()

                if Custom_Form.question_order == None:
                    Custom_Form.question_order = "address_form"
                else:
                    Custom_Form.question_order += f"/address_form"
            
        Custom_Form.save()
        new_question.custom_forms.add(custom_form_id)
        if new_question.answer_format[2:-2] == "multiple_choice":
            return redirect("build_question_select_choices", question_id = new_question.id, custom_form_id = custom_form_id)
        
    
    
    return render(request, 'form_builder/form_question_builder.html', {
        'form': build_question_form,
        'preview': img_src,
        'custom_form_id': custom_form_id,
        'warning' : ''
    })


    
def build_question_select_choices(request, custom_form_id, question_id):
    (question_id)
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
        (new_options_added.answer_format)

        answer_option_form = Answer_option_form(question_to_edit)
    return render(request, "form_builder/multiple_choice_builder.html", {
        "custom_form_id" : custom_form_id,
        "question_id" : question_id,
        'form' : answer_option_form,
        'question' : question_to_edit.question
    })



def build_question_success(request, custom_form_id):
    return render(request, 'form_builder/build_question_success.html', {
        'custom_form_id': custom_form_id
    })        


        
def fill_out_form(request, custom_form_id, current_form , back): 
    custom_form = Custom_Form.objects.get(id = 5)
    if custom_form.question_order == "" or custom_form.question_order is None:
        return redirect("build_question_view", custom_form_id = custom_form_id)

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
                    (request.POST) 
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
    current_custom_form = Custom_Form.objects.get(id = custom_form_id)
    question_array = current_custom_form.question_order.split("/")
    for i in range(0, len(question_array)):
        question_order[question_array[i]] = str(i)
       
    
    forms = {}
    questions = Question.objects.all()
    
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
        (current_form, last_form)
        return redirect('view_question_submitted', 2)
    
    
    return render(request, 'form_builder/fill_out_form.html', {
        'forms' : forms,
        'last_form' : last_form,
        'current_form' : current_form,
        'custom_form_id': custom_form_id
    })



def view_question_submitted(request, custom_form_id):
    
    req_energy = {
        "question": "Does the home consume a lot of energy, leading to costly energy bills?",
        "answer_for_approval" : "yes"
    }
    req_home = {
        "question" : "address_form",
        "field": "city",
        "expected"  :"Memphis"
    }

    req_renter = {
        "question" : "Which of the following best describes you?",
        "answer_for_approval" : "I am a renter"
    }
    
    req_income = {
        "question" : "What is your yearly household income?",
        "answer_for_approval" : "<45000"
    }
    req_build_date = {
        "question" : "When was your home built?",
        "answer_for_approval" : "Before 1978"
    }
    req_family_size = {
        "question" : "How many people live in your home?",
        "answer_for_approval" : ">3"
    }
    req_roof = {
        "question" : "Does the roof in your home have any problems?",
        "answer_for_approval" : "no"
    }
    req_yes_roof = {
        "question" : "Does the roof in your home have any problems?",
        "answer_for_approval" : "yes"
    }
    req_lead = {
        "question" : "Has anyone in the household tested positive for lead poisoning?",
        "answer_for_approval" : "no"
    }
    req_yes_plumbing = {
        "question" : "Does the plumbing of your home have any problems?",
        "answer_for_approval" : "yes"
    }
    req_child ={
        "question" : "Do you have any children born before 01-01-2000?",
        "answer_for_approval" : "yes"
    }
    req_chipping_paint = {
        "question" : "Is paint coming off any walls or surface?",
        "answer_for_approval" : "yes"
    }
    req_yes_HVAC = {
        "question" : "Does the heating, cooling, or ventilation (HVAC) of your home have any problems?",
        "answer_for_approval" : "yes"
    }
    req_accessibility = {
        "question" : "Does your home need upgrades to help someone with a physical disability?",
        "answer_for_approval" : "yes"
    }
    statement_energy = {
         "statement": "A high energy burden",
         "requirements" : [req_energy]
    }
    statement_home = {
        "statement": "You rent or own a home in Shelby County",
        "requirements" : [req_home]
    }
    statement_family_income = {
        "statement" : "Your yearly household income is less than IncomeLevel for a family of FamilySize",
        "requirements" : [req_income, req_family_size]
    }
    statement_structural = {
        "statement" : "Your home does not have any serious structural issues",
        "requirements" : [req_roof]
    }
    statement_lead = {
        "statement" : "Your home does not have any known lead hazards",
        "requirements" : [req_lead]
    }
    statement_build_date = {
        "statement" : "Your home was built before 1/1/1978",
        "requirements" : [req_build_date]
    }
    statement_paint = {
        "statement" : "Deteriorating or chipping paint",
        "requirements" : [req_chipping_paint]
    }
    statement_child_lead = {
        "statement" : "A child who visits or lives in the home and is under the age of 6 has tested positive for lead poisoning",
        "requirements" : [req_child, req_lead]
    }
    statement_renter = {
        "statement" : "Deteriorating or chipping paint",
        "requirements" : [req_renter]
    }
    statement_issues_roof = {
        "statement" : "Issues with roof",
        "requirements" : [req_yes_roof]
    }
    statement_issues_plumbing = {
        "statement" : "Issues with plumbing",
        "requirements" : [req_yes_plumbing]
    }
    statement_issues_HVAC = {
        "statement" : "Issues with plumbing Issues with heating, cooling, and ventilation (HVAC)",
        "requirements" : [req_yes_HVAC]
    }
    statement_energy_bills = {
        "statement" : "High energy bills",
        "requirements" : [req_energy]
    }
    statement_issues_accessibility = {
        "statement" : "Issues with accessibility",
        "requirements" : [req_accessibility]
    }
    statement_no_lead = {
        "statement" : "Your home does not have any known lead hazards",
        "requirements" : [req_lead]
    }
    need_id = {
        "statement" : "Government issued ID"
    }
    need_income = {
        "statement" : "Proof of income for the past 3 months"
    }
    need_energy = {
        "statement" : "Energy bills for the past 3 months"
    }
    need_residence = {
        "statement" : "Proof of homeownership or residence"
    }
    need_homeowner_insurance = {
        "statement" : "Proof of homeownership insurance"
    }
    need_mortgage = {
        "statement" : "Current Mortgage Statement"
    }
    need_birth_certificate = {
        "statement" : "Birth certificates of any children under six"
    }

    need_fee = {
        "statement" : "$250 application fee (paid online)"
    }
    need_25_fee = {
        "statement" : "$25 credit history fee (paid online)"
    }
    need_30_fee = {
        "statement" : "$30 credit history fee (paid online)"
    }
    need_25_40_fee = {
        "statement" : "$25 course fee per individual, $40 per couple"
    }
    ad_req_mortgage = {
        "statement" : "You must be up to date on mortgage payments"
    }
    ad_req_taxes = {
        "statement" : "You must be up to date on property taxes"
    }
    ad_req_weather = {
        "statement" : "Your home must not have been weatherized in the past 15 years"
    }
    
    ad_req_insurance = {
        "statement" : "You must have homeowners insurance"
    }

    ad_req_credit_score = {
        "statement" : "You must have a minimum credit score of 620"
    }

    ad_req_bankruptcy = {
        "statement" : "You must be discharged or dismissed of any  bankruptcy charges over the last 2 years"
    }

    call_weather = {
        "number" : "(901)-636-7366"
    }
    email_weather = {
        "email" : "weatherization@memphistn.gov"
    } 
    call_lead = {
        "number" : "(901)-636-LEAD(5323)"
    }
    email_lead = {
        "email" : "weatherization@memphistn.gov"
    }
    call_rental = {
        "number" : "(901) 728-6936"
    }
    call_home_improvement = {
        "number" : "901) 272-1122"
    }
    email_rental = {
        "email" : "mcclelland@uhinc.org"
    }
    Weatherization = {
        "title": "Weatherization",
        "description": 
            "WAP is a program designed to assist low-income households in reducing their fuel costs while contributing to national energy conservation through increased energy efficiency and consumer education. Weatherization work can include various types of insulation, air sealing, duct sealing, caulking, weather stripping, lighting upgrades, HVAC replacements and window replacements. Weatherization can reduce energy bills by as much as 25%.",
        "why_its_recommended": [[True, statement_energy]],
        "eligibility_requirements" : 
             [[True,statement_home], [True,statement_family_income], [True,statement_structural], [True,statement_lead]],
        "additional_requirements": [ad_req_weather],
        "what_you_need_to_apply":
            [need_id, need_income, need_energy, need_residence],
        "what_to_expect_after_applying":
            "The City has 90 days to approve or deny the application. If your application is approved, a certified auditor will visit your home to perform an energy audit resulting in a work order with a list of recommended weatherization measures. However, please note that due to high demand, priority will be given to persons with disability, and the elderly. In addition, homes may be deferred due to poor structural conditions.",
        "need_help" : { "call" : call_weather, "email" : email_weather},
        "eligible" : True       
    }

    Lead_Mitigation = {
        "title" : "Lead Mitigation",
        "description" :
            "The City of Memphis provides funding (in the form of a forgivable loan) to test and remediate lead hazards from the home. Lead is an environmental hazard that causes long term learning disabilities, such as brain damage, lower IQ levels, hyperactivity, and potent neurotoxins, especially in children. Deteriorating or chipping paint is a common source of lead poisoning in homes built before 1978.",
        "why_its_recommended": [[True, statement_build_date],[True, statement_paint],[True, statement_child_lead]],
        "eligibility_requirements" : 
             [[True,statement_home], [True,statement_build_date], [True,statement_paint], [True,statement_child_lead],[True, statement_family_income], [True, statement_structural]],
        "additional_requirements": 
             [ad_req_taxes, ad_req_mortgage],
        "what_you_need_to_apply":
            [need_id, need_income, need_homeowner_insurance, need_mortgage, need_birth_certificate],
        "what_to_expect_after_applying":
            "City has 90 days to approve or deny the application. If your application is approved, an inspector will be sent to evaluate the condition of the house. Next, an environmental consultant will do a lead inspection and lead test the paint, dust, and soil. Blood lead testing from the Shelby County Health Department may also be performed on any children under the age of 6. HCD will coordinate with you when it is your turn. However, please note that due to high demand, priority will be given to families with pregnant household members or children under the age of 6. In addition, homes may be deferred due to poor structural conditions.",
        "need_help" : { "call" : call_lead, "email" : email_lead},
        "eligible" : True       
    }
    Rental_Preservation = {
        "title" : "Rental Preservation Loan",
        "description" :
            "The United Housing Rental Preservation Loan offers $10,000-$80,000 at a fixed interest rate and a five year term with ten year amortization. The loan covers repairs and upgrades to rental property to preserve affordable quality housing for renters.",
        "why_its_recommended": [[]],
        "eligibility_requirements" : 
            [[True, statement_home],[True, statement_renter]],
        "additional_requirements": 
             [ad_req_taxes, ad_req_mortgage, ad_req_insurance, ad_req_credit_score, ad_req_bankruptcy],
        "what_you_need_to_apply":
            [need_id, need_fee],
        "what_to_expect_after_applying":
            "You will be contacted within 3-10 business days to discuss next steps for your application.",
        "need_help" : { "call" : call_rental, "email" : email_rental},
        "eligible" : True       
    }
    Home_Improvement = {
        "title" : "Home Improvement Loan",
        "description" :
            "The United Housing Home Improvement Loan offers $5,000-$15,000 at a low fixed interest rate and a 10 year term. The loan can be used for improvements like roofing upgrades, HVAC installations, weatherization, safety upgrades, accessibility features, and more.",
        "why_its_recommended": [[True, statement_issues_roof],[True, statement_issues_plumbing],[True, statement_issues_HVAC],[True, statement_energy_bills],[True, statement_issues_accessibility]],
        "eligibility_requirements" : 
            [[True, statement_home],[True, statement_family_income],[True, statement_issues_roof],[True, statement_issues_plumbing],[True, statement_issues_HVAC],[True, statement_energy_bills],[True, statement_issues_accessibility], [True, statement_no_lead]],
        "additional_requirements": 
             [ad_req_taxes, ad_req_mortgage, ad_req_insurance, ad_req_credit_score, ad_req_bankruptcy],
        "what_you_need_to_apply":
            [need_id, need_fee],
        "what_to_expect_after_applying":
            "You will be contacted within 3-10 business days to discuss next steps for your application.",
        "need_help" : { "call" : call_home_improvement, "email" : ""},
        "eligible" : True       
    }

    Rental_Counseling  = {
        "title" : "Rental Counseling",
        "description":
            "Work one-on-one with a United Housing counselor to build financial security and avoid eviction through: budget and credit coaching,breaking down the terms and conditions of your lease, connecting you to financial resources. What You’ll Need to Apply $25 credit history fee (paid online) What to Expect After Applying Within 24-72 hours, someone from UHI will contact you to schedule a 1 hour appointment.",
        "why_its_recommended":[[]],
        "eligibility_requirements": [[]],
        "additional_requirements": [[]],
        "what_you_need_to_apply": 
            [need_25_fee],
        "what_to_expect_after_applying":
            "Within 24-72 hours, someone from UHI will contact you to schedule a 1 hour appointment.",
        "need_help" : {"call" : "", "email": ""},
        "eligible": True
    }
    Money_Management  = {
        "title" : "Money Management Course",
        "description":
            "The eHome Money Management Course is an online, on-demand, 2-hour course that empowers you to: understand savings and spending, understand credit, and manage personal finances",
        "why_its_recommended":[[]],
        "eligibility_requirements": [[]],
        "additional_requirements": [[]],
        "what_you_need_to_apply": 
            [need_30_fee],
        "what_to_expect_after_applying":
            "You can begin the course immediately. Once you finish the course, you will need to schedule a 1 hour time to speak with a housing counselor in order to receive a certificate of completion for the course.",
        "need_help" : {"call" : "", "email": ""},
        "eligible": True
    }
    Homebuyer_education  = {
        "title" : "Homebuyer Education Course",
        "description":
            "The United Housing Homebuyer Education Course is an 8 hour course with a live English-speaking instructor*. The course covers many important topics to prepare for buying a home: Credit profile management, The importance of credit, How to improve credit over time, The different laws that regulate the use of credit, How to qualify for a mortgage loan, Selecting a house, Working with a Realtor, Home construction, Basic home maintenance, What happens at the loan closing, Predatory lenders and foreclosure ",
        "why_its_recommended":[[]],
        "eligibility_requirements": [[]],
        "additional_requirements": [[]],
        "what_you_need_to_apply": 
            [need_25_40_fee],
        "what_to_expect_after_applying":
            "Within 24-72 hours, someone from UHI will contact you to have you sign a disclosure agreement and fill out an assessment.",
        "need_help" : {"call" : "", "email": ""},
        "eligible": True
    }
    programs_list = [Weatherization, Lead_Mitigation, Rental_Preservation, Home_Improvement, Rental_Counseling, Money_Management, Homebuyer_education,]
   

    custom_form = Custom_Form.objects.get(id = 5)
    questions_submitted = []
    
    questions = Question.objects.all()

    QandA = {} # added for test

    for question in questions:
        if question.answer is not None:
            questions_submitted.append(question)
            QandA[question.question] = question.answer  #added for test

    address_submitted = [{'fields' : ""}]

    if custom_form.question_order:
        array_order = custom_form.question_order.split("/")
        (array_order)
        if 'address_form' in array_order:
            address_submitted = serializers.serialize( "python", Address.objects.all() )
            QandA["address_form"] = address_submitted #added for test
        

    for i in range(len(programs_list)):
        recommend_program = True
        for statement in programs_list[i]["why_its_recommended"]:
            if len(statement) > 0:
                for r in statement[1]["requirements"]:
                    if "field" in r.keys():
                        if QandA["address_form"][-1]["fields"][r["field"]] != r["expected"]:
                            recommend_program = False
                    elif r["answer_for_approval"][0] == ">" or r["answer_for_approval"][0] == "<":
                        if r["answer_for_approval"][0] == ">":
                            if QandA[r["question"]] <= int(r["answer_for_approval"][1:]):
                                recommend_program = False
                        elif r["answer_for_approval"][0] == "<":
                            if QandA[r["question"]] >= int(r["answer_for_approval"][1:]):
                                recommend_program = False

                    elif QandA[r["question"]] != r["answer_for_approval"]:
                        recommend_program = False
        
        eligible = True
        for j in range(len(programs_list[i]["eligibility_requirements"])):
            approved = True
            if len(programs_list[i]["eligibility_requirements"][j]) > 0:
                for r in programs_list[i]["eligibility_requirements"][j][1]["requirements"]:    
                    if "field" in r.keys():
                        if QandA["address_form"][-1]["fields"][r["field"]] != r["expected"]:
                            approved = False
                    elif r["answer_for_approval"][0] == ">" or r["answer_for_approval"][0] == "<":
                        
                        if r["answer_for_approval"][0] == ">":
                            if int(QandA[r["question"]]) <= int(r["answer_for_approval"][1:]):
                                approved = False
                        elif r["answer_for_approval"][0] == "<":
                            if int(QandA[r["question"]]) >= int(r["answer_for_approval"][1:]):
                                approved = False
                    
                    elif QandA[r["question"]] != r["answer_for_approval"]:
                        approved = False
                
                programs_list[i]["eligibility_requirements"][j][0] = approved
                
            if approved == False:
                eligible = False
        programs_list[i]["eligible"] = eligible

    income_level = False
    family_size = 0
   

    address_submitted = [{'fields' : ""}]
    if custom_form.question_order:
        array_order = custom_form.question_order.split("/")
        (array_order)
        if 'address_form' in array_order:
            address_submitted = serializers.serialize( "python", Address.objects.all() )
            QandA["address_form"] = address_submitted #added for test
        else:
            Address_objects = Address.objects.all()
            for address in Address_objects:
                address.delete()


    program_list_view = []
    i = 0
    for program in programs_list:
        new_program = []
        for key in program:
            new_catagory = []
            if key == "title" or key == "description" or key == "what_to_expect_after_applying" or key == "eligible":
                new_catagory.append(program[key])
            elif key == "why_its_recommended" or key == "eligibility_requirements":
                for statement in program[key]: 
                    new_statement = []
                    if len(statement) > 0:
                        new_statement.append(statement[0])
                        new_statement.append(statement[1]["statement"])
                    new_catagory.append(new_statement)
            elif key == "what_you_need_to_apply" or key == "additional_requirements":
                for statement in program[key]:
                    if len(statement) > 0:
                        new_catagory.append(statement["statement"])
            elif key == "need_help":
                if program[key]["call"]:
                    new_catagory.append(program[key]["call"]["number"])
                else:
                    new_catagory.append("")
                if program[key]["email"]:
                    new_catagory.append(program[key]["email"]["email"])
                else:
                    new_catagory.append("")

            new_program.append(new_catagory)
          
        
        program_list_view.append(new_program)
    
   
    for i in range(0, len(program_list_view)):
        program_list_view[i].append(i)
        print(program_list_view[i][8])
    
    return render(request, 'form_builder/view_question_submitted.html',{
        "program_list" : program_list_view,
        'questions_submitted': questions_submitted,
        'address_submitted' : address_submitted[0]['fields'],
        'family_size' : family_size,
        'custom_form_id': custom_form_id,
        
    } )


    

def custom_form_options(request, custom_form_id):
    
    return render(request, 'form_builder/custom_form_options.html',{
        'custom_form_id' : custom_form_id
    })

def question_organizer(request, custom_form_id, order_or_remove):
    
    if request.method == "POST":
        
        custom_form = Custom_Form.objects.get(id = custom_form_id)
        Custom_Form.question_order = "/".join(request.POST.getlist('current_location'))
        Custom_Form.save()
        

    custom_form = Custom_Form.objects.get(id = custom_form_id)
    current_question_order = custom_form.question_order
   
    question_array = current_question_order.split("/") 
    remove_form = Remove_form(question_array)
    q_dict = {}

    for i in range(len(question_array)):
        q_dict[i] = question_order_selector(i, question_array)

    return render(request, 'form_builder/question_organizer.html',{
        'forms': q_dict,
        'remove_form' : remove_form,
        'order_or_remove' : order_or_remove
    })

def question_remove(request, custom_form_id):
    if request.method == "POST":
       
        custom_form = Custom_Form.objects.get(id = custom_form_id)
        question_array = Custom_Form.question_order.split('/')
        (question_array)
        for question in question_array:
            if question == request.POST['current_location']:
                question_array.remove(question)
                if question == 'address_form':
                    address_forms = Address.objects.all()
                    for form in address_forms:
                        form.delete()
                    Question.objects.filter(answer_format = "['address_form']").delete()

                Question.objects.filter(question = question).delete()
                
        Custom_Form.question_order = ("/").join(question_array)
        Custom_Form.save()
        
                
        
        
        # Custom_Form.save()
        # (Custom_Form.question_order)

    custom_form = Custom_Form.objects.get(id = custom_form_id)
    current_question_order = Custom_Form.question_order
   
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

