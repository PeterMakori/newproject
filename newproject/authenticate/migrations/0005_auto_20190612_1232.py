# Generated by Django 2.2.1 on 2019-06-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0004_auto_20190612_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendfeedback',
            name='to',
            field=models.BooleanField(default=False),
        ),
    ]