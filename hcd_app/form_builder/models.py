from django.db import models
from localflavor.us.models import USStateField
#choices for answer format

# Create your models here.


class Program(models.Model):
    title = models.CharField(max_length=50)
    question_order = models.CharField(max_length=10000, null=True, blank=True)

class Question(models.Model):
    question = models.CharField(max_length=250, null= True, blank= True)
    img = models.CharField(max_length=250, null= True, blank= True)
    answer = models.CharField(max_length=250,null=True, blank=True)
    answer_format = models.CharField(max_length=50, default='text field')
    programs = models.ManyToManyField(Program, blank=True, null=True)


class Address(models.Model):
    address_1 = models.CharField(("Street Address"), max_length=128)
    address_2 = models.CharField(("Street Address Line 2"), max_length=128, blank=True)

    city = models.CharField(("City"), max_length=64, default="Memphis")
    state = USStateField(("State"), default="TN")
    zip_code = models.CharField(("Zip Code"), max_length=5, default="38104")
    build_date = models.CharField(("Home Build Date"), max_length=128, default="1987")
    
    
    

