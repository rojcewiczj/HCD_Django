from form_builder import models
from django.contrib import admin


# Register your models here.
myModels = [models.Custom_Form, models.Question, models.Address, models.Program, models.Statement, models.Requirement]
admin.site.register(myModels)