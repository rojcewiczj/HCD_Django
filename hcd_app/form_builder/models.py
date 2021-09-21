from django.db import models

# Create your models here.


class Program(models.Model):
    title = models.CharField(max_length=50)

class Question(models.Model):
    question = models.CharField(max_length=250, null= True, blank= True)
    answer = models.CharField(max_length=250,null=True, blank=True)
    answer_format = models.CharField(max_length=50, default='text field')
    programs = models.ManyToManyField(Program, blank=True, null=True)
    
    

