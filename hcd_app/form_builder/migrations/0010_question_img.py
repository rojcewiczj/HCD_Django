# Generated by Django 3.2.7 on 2021-10-11 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_builder', '0009_rename_shippingaddress_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='img',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
