# Generated by Django 3.2.7 on 2021-10-04 02:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0009_alter_program_question_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='question_order',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250), size=8),
        ),
    ]
