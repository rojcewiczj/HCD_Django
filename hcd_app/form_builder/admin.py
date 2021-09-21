from form_builder import models
from django.contrib import admin


# Register your models here.
myModels = [models.Program, models.Question]
admin.site.register(myModels)