# Generated by Django 3.2.7 on 2021-09-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0003_question_answer_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]