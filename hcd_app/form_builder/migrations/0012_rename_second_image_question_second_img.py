# Generated by Django 3.2.7 on 2021-10-18 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0011_question_second_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='second_image',
            new_name='second_img',
        ),
    ]