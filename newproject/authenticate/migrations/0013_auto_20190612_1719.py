# Generated by Django 2.2.1 on 2019-06-12 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0012_auto_20190612_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sendfeedback',
            old_name='department',
            new_name='depart',
        ),
        migrations.RenameField(
            model_name='sendfeedback',
            old_name='faculty',
            new_name='facu',
        ),
    ]
