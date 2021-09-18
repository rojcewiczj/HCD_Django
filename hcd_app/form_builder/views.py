from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    forms = {
         'HCD_lead_mitigation': [{"question":"where do you live?", "answer": "memphis"}]
         }
    
    return render(request, "form_builder/index.html", {
        'building': True,
        "forms":  forms
    })