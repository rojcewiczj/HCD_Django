from django.db import models
from localflavor.us.models import USStateField
#choices for answer format

# Create your models here.

#form model
class Custom_Form(models.Model):
    title = models.CharField(max_length=50)
    question_order = models.CharField(max_length=10000, null=True, blank=True)

#question model, many to many with form
class Question(models.Model):
    question = models.CharField(max_length=250, null= True, blank= True)
    img = models.CharField(max_length=250, null= True, blank= True)
    second_img = models.CharField(max_length=250, null= True, blank= True)
    answer = models.CharField(max_length=250, null=True, blank=True)
    answer_format = models.CharField(max_length=50, default='text field')
    Custom_Forms = models.ManyToManyField(Custom_Form, blank=True, null=True)

# address model, currenly lacking a relationship with form
class Address(models.Model):
    address_1 = models.CharField(("Street Address"), max_length=128)
    address_2 = models.CharField(("Street Address Line 2"), max_length=128, blank=True)
    city = models.CharField(("City"), max_length=64, default="Memphis")
    state = USStateField(("State"), default="TN")
    zip_code = models.CharField(("Zip Code"), max_length=5, default="38104")
    build_date = models.CharField(("Home Build Date"), max_length=128, default="1987")

#model for program, contains fields which dont requite more objects to build
class Program(models.Model):
    title = models.CharField(max_length=250, null= True, blank= True)
    description = models.CharField(max_length=1000, null= True, blank= True)
    what_to_expect_after_applying = models.CharField(max_length=1000, null= True, blank= True)
    call = models.CharField(max_length=250, null= True, blank= True)
    email = models.CharField(max_length=250, null= True, blank= True)

#statement refers to a statment on the programs which will need validation, the category that the 
#statement will be used as is determined by the boolean fields
class Statement(models.Model):
    statement = models.CharField(max_length=500, null= True, blank= True)
    programs = models.ManyToManyField(Program, blank=True, null=True)
    why_its_recommended = models.BooleanField()
    eligibility_requirements = models.BooleanField()
    additional_requirements = models.BooleanField()
    what_you_need_to_apply =  models.BooleanField()

# a requirement is a question and expected answer that will be used to determine if a statment is showed with postive or negative outcome 
class Requirement(models.Model):
    question = models.CharField(max_length=500, null= True, blank= True)
    answer_for_approval = models.CharField(max_length=250, null= True, blank= True)
    statements = models.ManyToManyField(Statement, blank=True, null=True)


