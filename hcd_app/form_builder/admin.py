from form_builder import models
from django.contrib import admin


# Register your models here.
myModels = [models.Custom_Form, models.Question, models.Address]
admin.site.register(myModels)