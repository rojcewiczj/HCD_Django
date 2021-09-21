from django.db import models

# Create your models here.


class Program(models.Model):
    title = models.CharField(max_length=50)

class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    answer_format = models.CharField(max_length=50, default='text field')
    programs = models.ManyToManyField(Program, blank=True, null=True)
    
    

